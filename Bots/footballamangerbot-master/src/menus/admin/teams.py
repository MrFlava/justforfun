import enum
from botmanlib.validators import PhoneNumber
from botmanlib.menus import OneListMenu, ArrowAddEditMenu
from botmanlib.menus.helpers import add_to_db, group_buttons
from botmanlib.messages import send_or_edit
from formencode import validators
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, ConversationHandler

from src.menus.admin.games import TeamGamesMenu
from src.menus.admin.players import TeamPlayersMenu
from src.models import Team, DBSession, TeamLeague


def delete_refresh_job(context):
    user_id = context.user_data['user'].id
    for job in context.job_queue.get_jobs_by_name(f"refresh_teams_menu_job_{user_id}"):
        job.schedule_removal()


class TeamsMenu(OneListMenu):
    menu_name = "teams_menu"

    class States(enum.Enum):
        ACTION = 1
        ASK_LEAGUE = 2

    def entry(self, update, context):
        return super(TeamsMenu, self).entry(update, context)

    def query_objects(self, context):
        return DBSession.query(Team).all()

    def entry_points(self):
        return [CallbackQueryHandler(self.entry, pattern='^football_clubs$', pass_user_data=True)]

    def message_text(self, context, obj):

        if obj:
            message_text = "Футбольные клубы Украины" + '\n'
            message_text += f"Название: {obj.name}" + '\n'
            message_text += f"Город: {obj.city}" + '\n'
            message_text += f"Год основания: {obj.since}" + '\n'
            message_text += f"Лига: {obj.league_str()}" + '\n'
        else:
            message_text = "Нет никаких данных о командах!" + '\n'

        return message_text

    def delete_ask(self, update, context):
        return super(TeamsMenu, self).delete_ask(update, context)

    def center_buttons(self, context, o=None):
        buttons = []
        buttons.append(InlineKeyboardButton("Добавить команду", callback_data="add_team"))
        if o:
            buttons.append(InlineKeyboardButton("Редактировать данные команды", callback_data="edit_team"))
        return buttons

    def back_button(self, context):
        return InlineKeyboardButton("🔙 Back", callback_data=f"back_{self.menu_name}")

    def object_buttons(self, context, obj):

        buttons = []

        if obj:
                buttons.append(InlineKeyboardButton("Изменить принадлежность к лиге", callback_data='change_league'))
                buttons.append(InlineKeyboardButton("Игры с зарубежными командами", callback_data='games'))
                buttons.append(InlineKeyboardButton("Игроки", callback_data='players'))
                buttons.append(InlineKeyboardButton("Удалить команду", callback_data=f"delete_{self.menu_name}"))
        return group_buttons(buttons, 1)

    def ask_change_league(self, update, context):
        delete_refresh_job(context)
        user = context.user_data['user']
        buttons = []
        message_text = "Пожалуйста, выберите новую принадлежность к лиге"
        obj = self.selected_object(context)
        if obj:
            buttons.append([InlineKeyboardButton("Высшая лига", callback_data='league_highest')])
            buttons.append([InlineKeyboardButton("Первая лига", callback_data='league_first')])
            buttons.append([InlineKeyboardButton("Вторая лига", callback_data='league_second')])
            buttons.append([InlineKeyboardButton("Третья лига", callback_data='league_third')])
            buttons.append([InlineKeyboardButton("🔙 Back", callback_data=f'back_to_team')])
            send_or_edit(context, chat_id=user.chat_id, text=message_text, reply_markup=InlineKeyboardMarkup(buttons, resize_keyboard=True))

        return self.States.ASK_LEAGUE

    def set_change_league(self, update, context):
        league_str = update.callback_query.data.replace("league_", "")
        obj = self.selected_object(context)
        obj.league = TeamLeague[league_str]
        if not add_to_db(obj):
            return self.conv_fallback(context)
        self.send_message(context)
        return self.States.ACTION

    def back_to_team(self, update, context):
        self.send_message(context)
        return self.States.ACTION

    def additional_states(self):
        games = TeamGamesMenu(self)
        players = TeamPlayersMenu(self)
        add_team = TeamAddMenu(self)
        edit_team = TeamEditMenu(self)
        return {self.States.ACTION: [add_team.handler,
                                     edit_team.handler,
                                     players.handler,
                                     games.handler,
                                     CallbackQueryHandler(self.ask_change_league, pattern='^change_league$')],
                self.States.ASK_LEAGUE: [CallbackQueryHandler(self.back_to_team, pattern='^back_to_team$'),
                                         CallbackQueryHandler(self.set_change_league, pattern='^league_(highest|first|second|third)$')]}

    def after_delete_text(self, context):
        return "Команда удалена"


class TeamAddMenu(ArrowAddEditMenu):
    menu_name = 'team_add_menu'
    model = Team

    def entry(self, update, context):
        return super(TeamAddMenu, self).entry(update, context)

    def query_object(self, context):
        return None

    def fields(self, context):
        fields = [self.Field('name', "*Назвнаие", validators.String(), required=True),
                  self.Field('city', "*Город", validators.String(), required=True),
                  self.Field('since', "*Год основания", validators.Number(), required=True, default=0),
                  self.Field('manager_FIO', "*ФИО Председателя", validators.String(), required=True),
                  self.Field('contact_number', "*Контактный телефон", PhoneNumber, required=True)]
        return fields

    def entry_points(self):
        return [CallbackQueryHandler(self.entry, pattern="^add_team$")]

    def save_object(self, obj, context, session=None):
        user_data = context.user_data
        obj.name = user_data[self.menu_name]['name']
        obj.city = user_data[self.menu_name]['city']
        obj.since = user_data[self.menu_name]['since']
        obj.manager_FIO = user_data[self.menu_name]['manager_FIO']
        obj.contact_number = user_data[self.menu_name]['contact_number']

        if not add_to_db(obj, session):
            return self.conv_fallback(context)


class TeamEditMenu(ArrowAddEditMenu):
    menu_name = 'team_edit_menu'
    model = Team

    def entry(self, update, context):
        return super(TeamEditMenu, self).entry(update, context)

    def query_object(self, context):

        team = self.parent.selected_object(context)
        if team:
            return DBSession.query(Team).filter(Team.id == team.id).first()
        else:
            self.parent.update_objects(context)
            self.parent.send_message(context)
            return ConversationHandler.END

    def fields(self, context):
        fields = [self.Field('name', "*Назвнаие", validators.String(), required=True),
                  self.Field('city', "*Город", validators.String(), required=True),
                  self.Field('since', "*Год основания", validators.Number(), required=True, default=0),
                  self.Field('manager_FIO', "*ФИО Председателя", validators.String(), required=True),
                  self.Field('contact_number', "*Контактный телефон", PhoneNumber, required=True)]
        return fields

    def entry_points(self):
        return [CallbackQueryHandler(self.entry, pattern='^edit_team$')]




