import enum

from botmanlib.menus import OneListMenu
from botmanlib.messages import send_or_edit
from botmanlib.menus.helpers import group_buttons
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler


from src.models import DBSession, Player, Game, PlayerGame


class PlayersMenu(OneListMenu):
    menu_name = 'players_menu'
    model = Player
    auto_hide_arrows = True

    class States(enum.Enum):
        ACTION = 1
        ASK_GAME = 2

    def entry(self, update, context):
        if self.menu_name not in context.user_data:
            context.user_data[self.menu_name] = {}
        self._load(context)
        user = context.user_data['user']
        _ = user.translator
        self.send_message(context)
        if update.callback_query and update.callback_query.id:
            context.bot.answer_callback_query(update.callback_query.id)

        return self.States.ACTION

    def query_objects(self, context):
        team = self.parent.selected_object(context)
        return DBSession.query(Player).filter(Player.team_id == team.id).all()

    def entry_points(self):
        return [CallbackQueryHandler(self.entry, pattern='^players$', pass_user_data=True)]

    def message_text(self, context, obj):

            if obj:
                message_text = "Игроки" + '\n'
                message_text += f"ФИО: {obj.FIO}" + '\n'
                message_text += f"Положение в команде: {obj.position_str()}" + '\n'
                message_text += f"Дата рождения: {obj.date_of_birth.strftime('%d.%m.%Y ')}" + '\n'
                message_text += '\n'
                message_text += f"В команде с {obj.in_team_since} года" + '\n'
                message_text += f"Стоимость контракта: {obj.contract_value} UAH" + '\n'
            else:
                message_text = "Нет никаких данных о игроках!" + '\n'

            return message_text

    def back_button(self, context):
        return InlineKeyboardButton("🔙 Back", callback_data=f"back_{self.menu_name}")

    def object_buttons(self, context, obj):

        buttons = []

        if obj:
            buttons.append(InlineKeyboardButton("Участие в игре", callback_data='player_games'))
        return group_buttons(buttons, 1)

    def ask_game(self, update, context):
        user = context.user_data['user']
        team = self.parent.selected_object(context)
        game = DBSession.query(Game).filter(Game.team_id == team.id).first()
        player = self.selected_object(context)
        buttons = []
        player_game_aosc = DBSession.query(PlayerGame).get((player.id, game.id))
        message_text = "Участие в игре" + '\n'
        message_text += f"Денежная премия: {player_game_aosc.cash_bonus} UAH" + '\n'
        message_text += f"Нарушение: {player_game_aosc.player_violations_str()}" + '\n'
        buttons.append([InlineKeyboardButton("🔙 Back", callback_data=f'back_to_player')])
        send_or_edit(context, chat_id=user.chat_id, text=message_text, reply_markup=InlineKeyboardMarkup(buttons, resize_keyboard=True))
        return self.States.ASK_GAME

    def back_to_player(self, update, context):
        self.send_message(context)
        return self.States.ACTION

    def additional_states(self):
        return {
            self.States.ACTION: [CallbackQueryHandler(self.ask_game, pattern='^player_games$')],
            self.States.ASK_GAME: [CallbackQueryHandler(self.back_to_player, pattern='^back_to_player$')]}


