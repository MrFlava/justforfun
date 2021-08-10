import enum


from botmanlib.menus import OneListMenu
from botmanlib.menus.helpers import group_buttons

from telegram import InlineKeyboardButton
from telegram.ext import CallbackQueryHandler

from src.models import DogTrainingClub, DBSession
from src.menus.start.dogs import ClubDogsMenu

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

    def back_button(self, context):
        return InlineKeyboardButton("🔙 Назад", callback_data=f"back_{self.menu_name}")

    def object_buttons(self, context, obj):

        buttons = []

        if obj:
                buttons.append(InlineKeyboardButton("Собаки кинологического кулба", callback_data='club_dogs'))
        return group_buttons(buttons, 1)

    def additional_states(self):
        club_dogs_menu = ClubDogsMenu(self)

        return {self.States.ACTION: [club_dogs_menu.handler]}

    def after_delete_text(self, context):
        return "Клуб удалён"
