import enum


from botmanlib.menus import OneListMenu
from botmanlib.menus.helpers import group_buttons
from botmanlib.messages import send_or_edit

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler


from src.models import DBSession, Dog, Competition, DogCompetitions


class ClubDogsMenu(OneListMenu):
    menu_name = 'club_dogs_menu'
    model = Dog

    class States(enum.Enum):
        ACTION = 1
        ASK_SOCIAL_POSITION = 2
        ASK_COMPETITION = 3

    def entry(self, update, context):
        return super(ClubDogsMenu, self).entry(update, context)

    def query_objects(self, context):
        club = self.parent.selected_object(context)
        return DBSession.query(Dog).filter(Dog.dog_training_club_id == club.id).all()

    def entry_points(self):
        return [CallbackQueryHandler(self.entry, pattern='^club_dogs$', pass_user_data=True)]

    def message_text(self, context, obj):

            if obj:
                message_text = "Собаки кинологического клуба и их хозяева" + '\n'
                message_text += f"Кличка: {obj.nickname}" + '\n'
                message_text += f"Порода: {obj.breed}" + '\n'
                message_text += f"Год рождения: {obj.year}" + '\n'
                message_text += f"Цена за щенка: {obj.price} UAH" + '\n'
                message_text += '\n'
                message_text += f"ФИО хозяина: {obj.FIO}" + '\n'
                message_text += f"Социальное положение: {obj.social_position.to_str()}" + '\n'
                message_text += f"Дата рождения: {obj.date_of_birth.strftime('%d.%m.%Y')}" + '\n'
                message_text += f"Адрес: {obj.address}" + '\n'
            else:
                message_text = "Нет никаких данных о собаках этого кинологического клуба!" + '\n'

            return message_text

    def back_button(self, context):
        return InlineKeyboardButton("🔙 Назад", callback_data=f"back_{self.menu_name}")

    def object_buttons(self, context, obj):

        buttons = []

        if obj:
            buttons.append(InlineKeyboardButton("Участие в соревнованиях", callback_data='dog_competitions'))
            buttons.append(InlineKeyboardButton("Удалить данные собаки", callback_data=f"delete_{self.menu_name}"))
        return group_buttons(buttons, 1)

    def ask_competition(self, update, context):
        user = context.user_data['user']
        club = self.parent.selected_object(context)
        competition = DBSession.query(Competition).filter(Competition.club_id == club.id).first()
        dog = self.selected_object(context)
        buttons = []
        dog_competition_aosc = DBSession.query(DogCompetitions).get((dog.id, competition.id))
        if dog_competition_aosc:
            message_text = "Участие в сореввновании" + '\n'
            message_text += f"Название: {competition.date.strftime('%d.%m.%Y ')}" + '\n'
            message_text += f"Дата проведения: {competition.date.strftime('%d.%m.%Y ')}" + '\n'
            message_text += f"Взнос: {competition.contributiont}" + '\n'
            message_text += f"Кол-во зрителей: {competition.viewers_quantity}" + '\n'
            message_text += f"Награда: {dog_competition_aosc.reward}" + '\n'
        else:
            message_text = "Данные о соревнованиях отсутствуют!"
        buttons.append([InlineKeyboardButton("🔙 Back", callback_data=f'back_to_dog')])
        send_or_edit(context, chat_id=user.chat_id, text=message_text, reply_markup=InlineKeyboardMarkup(buttons, resize_keyboard=True))
        return self.States.ASK_COMPETITION

    def back_to_dog(self, update, context):
        self.send_message(context)
        return self.States.ACTION

    def additional_states(self):

        return {self.States.ACTION: [CallbackQueryHandler(self.ask_competition, pattern='^dog_competitions$')],
                        self.States.ASK_COMPETITION: [CallbackQueryHandler(self.back_to_dog, pattern='^back_to_dog$')]}

