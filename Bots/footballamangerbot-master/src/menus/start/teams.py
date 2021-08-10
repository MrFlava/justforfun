
from botmanlib.menus import OneListMenu
from botmanlib.menus.helpers import group_buttons

from telegram import InlineKeyboardButton
from telegram.ext import CallbackQueryHandler

from src.models import Team, DBSession
from src.menus.start.players import PlayersMenu
from src.menus.start.games import UserTeamGamesMenu


class TeamMenu(OneListMenu):
    menu_name = 'team_menu'
    model = Team
    auto_hide_arrows = True

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
        return DBSession.query(Team).all()

    def entry_points(self):
        return [CallbackQueryHandler(self.entry, pattern='^football_clubs$')]

    def message_text(self, context, obj):
        user = context.user_data['user']

        if obj:
            message_text = "Футбольные клубы Украины" + '\n'
            message_text += f"Название: {obj.name}" + '\n'
            message_text += f"Город: {obj.city}" + '\n'
            message_text += f"Год основания: {obj.since}" + '\n'
            message_text += f"Лига: {obj.league_str()}" + '\n'
        else:
            message_text = "Нет никаких данных о командах!" + '\n'

        return message_text

    def back_button(self, context):
        user = context.user_data['user']
        _ = user.translator
        return InlineKeyboardButton(_("🔙 Back"), callback_data=f"back_{self.menu_name}")

    def object_buttons(self, context, obj):
        user = context.user_data['user']
        _ = user.translator
        buttons = []

        if obj:
            buttons.append(InlineKeyboardButton("Игры с зарубежными командами", callback_data='games'))
            buttons.append(InlineKeyboardButton("Игроки", callback_data='players'))
        return group_buttons(buttons, 1)

    def additional_states(self):
        players_menu = PlayersMenu(self)
        games_menu = UserTeamGamesMenu(self)
        return {
            self.States.ACTION: [players_menu.handler,
                                 games_menu.handler]
        }




