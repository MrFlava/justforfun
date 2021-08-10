import enum
from formencode import validators
from botmanlib.menus import OneListMenu, ArrowAddEditMenu
from botmanlib.menus.helpers import to_state, group_buttons, add_to_db
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, TelegramError
from telegram.ext import ConversationHandler, CallbackQueryHandler, MessageHandler, Filters

from src.models import Book, User, DBSession
from src.settings import WEBHOOK_ENABLE


class BooksListMenu(OneListMenu):
    class States(enum.Enum):
        ACTION = 1

    menu_name = 'books_list_menu'
    model = Book
    disable_web_page_preview = False

    def entry(self, update, context):
        self._load(context)
        self.send_message(context)
        if update.callback_query:
            context.bot.answer_callback_query(update.callback_query.id)
        return self.States.ACTION

    def query_objects(self, context):
        return DBSession.query(Book).all()

    def entry_points(self):
        return [CallbackQueryHandler(self.entry, pattern='^list_of_books$', pass_user_data=True)]

    def message_text(self, context, obj):
        if obj:
            message_text = f"____{'Книги'}____\n"
            if obj.image is not None:
                message_text = f'<a href="{self.bot.get_image_url(obj.image)}">\u200B</a>' if obj and WEBHOOK_ENABLE else ""
            message_text += "Жанр" + f": {obj.genre}\n"
            message_text += "Название" + f": {obj.name}\n"
            message_text += "Описание" + f": {obj.description}\n"
            message_text += "Цена" + f": {obj.price}\n"

            message_text += "\n"
        else:
            message_text = "Упс, пока что данные о книгах отсутствуют. Попробуйте позже!" + '\n'

        return message_text

    def page_text(self, current_page, max_page, context):
        return "(" + "Страница" + ' ' + str(current_page) + ' ' + "из" + ' ' + str(max_page) + ")"

    def object_buttons(self, context, obj):
        user = context.user_data['user']
        buttons = []
        if obj and user.has_order is False:
            buttons.append(InlineKeyboardButton("Заказать книгу", url='https://drive.google.com/drive/folders/1y_g4zTIExBw738pVNdlJZnOyD98KVESr?usp=drive_open'))
        return group_buttons(buttons, 1)

    def additional_states(self):

        return {self.States.ACTION: []}
