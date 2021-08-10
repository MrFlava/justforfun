import enum
import datetime

from botmanlib.menus import OneListMenu, ArrowAddEditMenu
from botmanlib.menus.helpers import add_to_db, group_buttons
from botmanlib.messages import send_or_edit
from formencode import validators
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, ConversationHandler


from src.models import DBSession, Dog, Competition, DogCompetitions, SocialPosition


def delete_refresh_job(context):
    user_id = context.user_data['user'].id
    for job in context.job_queue.get_jobs_by_name(f"refresh_dogs_menu_job_{user_id}"):
        job.schedule_removal()


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

    def center_buttons(self, context, o=None):
        buttons = []
        buttons.append(InlineKeyboardButton("Добавить собаку", callback_data="add_dog"))
        if o:
            buttons.append(InlineKeyboardButton("Редактировать данные собаки", callback_data="edit_dog"))
        return buttons

    def object_buttons(self, context, obj):

        buttons = []

        if obj:
            buttons.append(InlineKeyboardButton("Изменить данные о социальном положении хозяина", callback_data='change_social_position'))
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

    def ask_change_social_position(self, update, context):
        delete_refresh_job(context)
        user = context.user_data['user']
        buttons = []
        message_text = "Пожалуйста, выберите новый социальный статус в хозяина"
        obj = self.selected_object(context)
        if obj:
            buttons.append([InlineKeyboardButton("Служащий", callback_data='pos_employee')])
            buttons.append([InlineKeyboardButton("Учащийся", callback_data='pos_student')])
            buttons.append([InlineKeyboardButton("Предприниматель", callback_data='pos_businessman')])
            buttons.append([InlineKeyboardButton("Пенсионер", callback_data='pos_pensioner')])
            buttons.append([InlineKeyboardButton("Рабочий", callback_data='pos_working')])
            buttons.append([InlineKeyboardButton("🔙 Назад", callback_data=f'back_to_dog')])
            send_or_edit(context, chat_id=user.chat_id, text=message_text, reply_markup=InlineKeyboardMarkup(buttons, resize_keyboard=True))

        return self.States.ASK_SOCIAL_POSITION

    def set_social_position(self, update, context):
        pos_str = update.callback_query.data.replace("pos_", "")
        obj = self.selected_object(context)
        obj.social_position = SocialPosition[pos_str]
        if not add_to_db(obj):
            return self.conv_fallback(context)
        self.send_message(context)
        return self.States.ACTION

    def back_to_dog(self, update, context):
        self.send_message(context)
        return self.States.ACTION

    def additional_states(self):
        add_dog = DogAddMenu(self)
        edit_edit = DogEditMenu(self)
        return {self.States.ACTION: [add_dog.handler,
                                     edit_edit.handler,
                                     CallbackQueryHandler(self.ask_change_social_position, pattern='^change_social_position$'),
                                     CallbackQueryHandler(self.ask_competition, pattern='^dog_competitions$')
                                     ],
                self.States.ASK_SOCIAL_POSITION: [CallbackQueryHandler(self.back_to_dog, pattern='^back_to_dog$'),
                                                  CallbackQueryHandler(self.set_social_position, pattern='^pos_(employee|student|businessman|pensioner|working)$')],
                self.States.ASK_COMPETITION: [CallbackQueryHandler(self.back_to_dog, pattern='^back_to_dog$')]}

    def after_delete_text(self, context):
        return "Данные собаки удалены"


class DogAddMenu(ArrowAddEditMenu):
    menu_name = 'dog_add_menu'
    model = Dog

    def entry(self, update, context):
        return super(DogAddMenu, self).entry(update, context)

    def query_object(self, context):
        return None

    def fields(self, context):
        year = datetime.datetime.now().year
        fields = [self.Field('nickname', "*Кличка", validators.String(), required=True),
                  self.Field('breed', "*Порода", validators.String(), required=True),
                  self.Field('year', "*Год рождения", validators.Number(min=1, max=year), required=True, default=0),
                  self.Field('price', "*Цена за щенка", validators.Number(min=1), required=True, default=0),
                  self.Field('FIO', "*ФИО хозяина", validators.String(), required=True),
                  self.Field('date_of_birth', "*Дата рождения", validators.DateConverter()),
                  self.Field('address', "*Адрес", validators.String(), required=True)]
        return fields

    def entry_points(self):
        return [CallbackQueryHandler(self.entry, pattern="^add_dog$")]

    def save_object(self, obj, context, session=None):
        user_data = context.user_data
        obj.nickname = user_data[self.menu_name]['nickname']
        obj.breed = user_data[self.menu_name]['breed']
        obj.year = user_data[self.menu_name]['year']
        obj.price = user_data[self.menu_name]['price']
        obj.FIO = user_data[self.menu_name]['FIO']
        obj.date_of_birth = user_data[self.menu_name]['date_of_birth']
        obj.address = user_data[self.menu_name]['address']
        obj.dog_training_club = self.parent.parent.selected_object(context)

        if not add_to_db(obj, session):
            return self.conv_fallback(context)


class DogEditMenu(ArrowAddEditMenu):
    menu_name = 'dog_edit_menu'
    model = Dog

    def entry(self, update, context):
        return super(DogEditMenu, self).entry(update, context)

    def query_object(self, context):

        dog = self.parent.selected_object(context)
        if dog:
            return DBSession.query(Dog).filter(Dog.id == dog.id).first()
        else:
            self.parent.update_objects(context)
            self.parent.send_message(context)
            return ConversationHandler.END

    def fields(self, context):
        year = datetime.datetime.now().year
        fields = [self.Field('nickname', "*Кличка", validators.String(), required=True),
                  self.Field('breed', "*Порода", validators.String(), required=True),
                  self.Field('year', "*Год рождения", validators.Number(min=1, max=year), required=True, default=0),
                  self.Field('price', "*Цена за щенка", validators.Number(min=1), required=True, default=0),
                  self.Field('FIO', "*ФИО хозяина", validators.String(), required=True),
                  self.Field('date_of_birth', "*Дата рождения", validators.DateConverter()),
                  self.Field('address', "*Адрес", validators.String(), required=True)]
        return fields

    def entry_points(self):
        return [CallbackQueryHandler(self.entry, pattern="^edit_dog$")]




