import enum

from botmanlib.menus import OneListMenu, ArrowAddEditMenu
from botmanlib.menus.helpers import add_to_db, group_buttons
from botmanlib.messages import send_or_edit
from formencode import validators
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, ConversationHandler


from src.models import DBSession, Player, PlayerPosition, PlayerGame, Game


def delete_refresh_job(context):
    user_id = context.user_data['user'].id
    for job in context.job_queue.get_jobs_by_name(f"refresh_players_menu_job_{user_id}"):
        job.schedule_removal()


class TeamPlayersMenu(OneListMenu):
    menu_name = 'team_players_menu'
    model = Player

    class States(enum.Enum):
        ACTION = 1
        ASK_POSITION = 2
        ASK_GAME = 3

    def entry(self, update, context):
        return super(TeamPlayersMenu, self).entry(update, context)

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

    def center_buttons(self, context, o=None):
        buttons = []
        buttons.append(InlineKeyboardButton("Добавить игрока", callback_data="add_player"))
        if o:
            buttons.append(InlineKeyboardButton("Редактировать данные игрока", callback_data="edit_player"))
        return buttons

    def object_buttons(self, context, obj):

        buttons = []

        if obj:
            buttons.append(InlineKeyboardButton("Изменить положение в команде", callback_data='change_position'))
            buttons.append(InlineKeyboardButton("Участие в игре", callback_data='player_games'))
            buttons.append(InlineKeyboardButton("Удалить данные игрока", callback_data=f"delete_{self.menu_name}"))
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

    def ask_change_position(self, update, context):
        delete_refresh_job(context)
        user = context.user_data['user']
        buttons = []
        message_text = "Пожалуйста, выберите новое положение в команде"
        obj = self.selected_object(context)
        if obj:
            buttons.append([InlineKeyboardButton("На замене", callback_data='position_reserve_player')])
            buttons.append([InlineKeyboardButton("Вратарь", callback_data='position_goalkeeper')])
            buttons.append([InlineKeyboardButton("Атакующий", callback_data='position_attack')])
            buttons.append([InlineKeyboardButton("Капитан", callback_data='position_captain')])
            buttons.append([InlineKeyboardButton("Защитник", callback_data='position_defender')])
            buttons.append([InlineKeyboardButton("Полузащитник", callback_data='position_midfielder')])
            buttons.append([InlineKeyboardButton("🔙 Back", callback_data=f'back_to_player')])
            send_or_edit(context, chat_id=user.chat_id, text=message_text,reply_markup=InlineKeyboardMarkup(buttons, resize_keyboard=True))

        return self.States.ASK_POSITION

    def set_change_position(self, update, context):
        position_str = update.callback_query.data.replace("position_", "")
        obj = self.selected_object(context)
        obj.position = PlayerPosition[position_str]
        if not add_to_db(obj):
            return self.conv_fallback(context)
        self.send_message(context)
        return self.States.ACTION

    def back_to_player(self, update, context):
        self.send_message(context)
        return self.States.ACTION

    def additional_states(self):
        add_player = PlayerAddMenu(self)
        edit_player = PlayerEditMenu(self)
        return {self.States.ACTION: [add_player.handler,
                                     edit_player.handler,
                                     CallbackQueryHandler(self.ask_change_position, pattern='^change_position$'),
                                     CallbackQueryHandler(self.ask_game, pattern='^player_games$')],
                self.States.ASK_POSITION: [CallbackQueryHandler(self.back_to_player, pattern='^back_to_player$'),
                                           CallbackQueryHandler(self.set_change_position, pattern='^position_(reserve_player|goalkeeper|attack|captain|defender|midfielder)$')],
                self.States.ASK_GAME: [CallbackQueryHandler(self.back_to_player, pattern='^back_to_player$')]}

    def after_delete_text(self, context):
        return "Данные игрока удалены"


class PlayerAddMenu(ArrowAddEditMenu):
    menu_name = 'player_add_menu'
    model = Player

    def entry(self, update, context):
        return super(PlayerAddMenu, self).entry(update, context)

    def query_object(self, context):
        return None

    def fields(self, context):

        fields = [self.Field('FIO', "*ФИО", validators.String(), required=True),
                  self.Field('date_of_birth', "Дата рождения", validators.DateConverter()),
                  self.Field('in_team_since', "*В команде с", validators.Number(), required=True, default=0),
                  self.Field('contract_value', "*Стоимость контракта", validators.Number(),  units=" " + "UAH")]
        return fields

    def entry_points(self):
        return [CallbackQueryHandler(self.entry, pattern="^add_player$")]

    def save_object(self, obj, context, session=None):
        user_data = context.user_data
        obj.FIO = user_data[self.menu_name]['FIO']
        obj.date_of_birth = user_data[self.menu_name]['date_of_birth']
        obj.in_team_since = user_data[self.menu_name]['in_team_since']
        obj.contract_value = user_data[self.menu_name]['contract_value']
        obj.team = self.parent.parent.selected_object(context)

        if not add_to_db(obj, session):
            return self.conv_fallback(context)


class PlayerEditMenu(ArrowAddEditMenu):
    menu_name = 'player_edit_menu'
    model = Player

    def entry(self, update, context):
        return super(PlayerEditMenu, self).entry(update, context)

    def query_object(self, context):

        player = self.parent.selected_object(context)
        if player:
            return DBSession.query(Player).filter(Player.id == player.id).first()
        else:
            self.parent.update_objects(context)
            self.parent.send_message(context)
            return ConversationHandler.END

    def fields(self, context):

        fields = [self.Field('FIO', "*ФИО", validators.String(), required=True),
                  self.Field('date_of_birth', "Дата рождения", validators.DateConverter()),
                  self.Field('in_team_since', "*В команде с", validators.Number(), required=True, default=0),
                  self.Field('contract_value', "*Стоимость контракта", validators.Number(), units=" " + "UAH")]
        return fields

    def entry_points(self):
        return [CallbackQueryHandler(self.entry, pattern="^edit_player$")]




