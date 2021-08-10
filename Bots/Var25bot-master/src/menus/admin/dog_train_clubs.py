import enum
import datetime

from botmanlib.validators import PhoneNumber
from botmanlib.menus import OneListMenu, ArrowAddEditMenu
from botmanlib.menus.helpers import add_to_db, group_buttons

from formencode import validators

from telegram import InlineKeyboardButton
from telegram.ext import CallbackQueryHandler, ConversationHandler

from src.models import DogTrainingClub, DBSession
from src.menus.admin.dogs import ClubDogsMenu
# from src.menus.admin. import


def delete_refresh_job(context):
    user_id = context.user_data['user'].id
    for job in context.job_queue.get_jobs_by_name(f"refresh_clubs_menu_job_{user_id}"):
        job.schedule_removal()


class DogTrainingClubsMenu(OneListMenu):
    menu_name = "dog_training_clubs_menu"

    class States(enum.Enum):
        ACTION = 1

    def entry(self, update, context):
        return super(DogTrainingClubsMenu, self).entry(update, context)

    def query_objects(self, context):
        return DBSession.query(DogTrainingClub).all()

    def entry_points(self):
        return [CallbackQueryHandler(self.entry, pattern='^dog_training_clubs$', pass_user_data=True)]

    def message_text(self, context, obj):

        if obj:
            message_text = "Кинологические клубы" + '\n'
            message_text += f"Название: {obj.name}" + '\n'
            message_text += f"Район города: {obj.district}" + '\n'
            message_text += f"Работает с: {obj.year}" + '\n'
            message_text += f"Телефон: {obj.phone}" + '\n'
            message_text += f"Вступительный взнос: {obj.entrance_fee}" + '\n'
        else:
            message_text = "Нет никаких данных о кинологических клубах!" + '\n'

        return message_text

    def delete_ask(self, update, context):
        return super(DogTrainingClubsMenu, self).delete_ask(update, context)

    def center_buttons(self, context, o=None):
        buttons = []
        buttons.append(InlineKeyboardButton("Добавить клуб", callback_data="add_club"))
        if o:
            buttons.append(InlineKeyboardButton("Редактировать кулб", callback_data="edit_club"))
        return buttons

    def back_button(self, context):
        return InlineKeyboardButton("🔙 Назад", callback_data=f"back_{self.menu_name}")

    def object_buttons(self, context, obj):

        buttons = []

        if obj:

                buttons.append(InlineKeyboardButton("Собаки кинологического кулба", callback_data='club_dogs'))
                buttons.append(InlineKeyboardButton("Удалить клуб", callback_data=f"delete_{self.menu_name}"))
        return group_buttons(buttons, 1)

    def additional_states(self):

        add_club = ClubAddMenu(self)
        edit_club = ClubEditMenu(self)
        club_dogs_menu = ClubDogsMenu(self)

        return {self.States.ACTION: [add_club.handler,
                                     edit_club.handler,
                                     club_dogs_menu.handler]}

    def after_delete_text(self, context):
        return "Клуб удалён"


class ClubAddMenu(ArrowAddEditMenu):
    menu_name = 'club_add_menu'
    model = DogTrainingClub

    def entry(self, update, context):
        return super(ClubAddMenu, self).entry(update, context)

    def query_object(self, context):
        return None

    def fields(self, context):
        year = datetime.datetime.now().year
        fields = [self.Field('name', "*Назвнаие", validators.String(), required=True),
                  self.Field('district', "*Район", validators.String(), required=True),
                  self.Field('year', "*Работает с", validators.Number(min=1, max=year), required=True, default=0),
                  self.Field('phone', "*Телефон", PhoneNumber, required=True),
                  self.Field('entrance_fee', "*Вступительный взнос", validators.Number(min=1), required=True)]
        return fields

    def entry_points(self):
        return [CallbackQueryHandler(self.entry, pattern="^add_club$")]

    def save_object(self, obj, context, session=None):
        user_data = context.user_data
        obj.name = user_data[self.menu_name]['name']
        obj.district = user_data[self.menu_name]['district']
        obj.year = user_data[self.menu_name]['year']
        obj.phone = user_data[self.menu_name]['phone']
        obj.entrance_fee = user_data[self.menu_name]['entrance_fee']

        if not add_to_db(obj, session):
            return self.conv_fallback(context)


class ClubEditMenu(ArrowAddEditMenu):
    menu_name = 'service_edit_menu'
    model = DogTrainingClub

    def entry(self, update, context):
        return super(ClubEditMenu, self).entry(update, context)

    def query_object(self, context):

        club = self.parent.selected_object(context)
        if club:
            return DBSession.query(DogTrainingClub).filter(DogTrainingClub.id == club.id).first()
        else:
            self.parent.update_objects(context)
            self.parent.send_message(context)
            return ConversationHandler.END

    def fields(self, context):
        year = datetime.datetime.now().year
        fields = [self.Field('name', "*Назвнаие", validators.String(), required=True),
                  self.Field('district', "*Район", validators.String(), required=True),
                  self.Field('year', "*Работает с", validators.Number(min=1, max=year), required=True, default=0),
                  self.Field('phone', "*Телефон", PhoneNumber, required=True),
                  self.Field('entrance_fee', "*Вступительный взнос", validators.Number(min=1), required=True)]
        return fields

    def entry_points(self):
        return [CallbackQueryHandler(self.entry, pattern='^edit_club$')]




