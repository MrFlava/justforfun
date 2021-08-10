from formencode import validators
from telegram import InlineKeyboardButton
from botmanlib.menus.helpers import add_to_db, group_buttons, require_permission
from botmanlib.menus import OneListMenu, ArrowAddEditMenu
from telegram.ext import CallbackQueryHandler, ConversationHandler

from src.models import Book, DBSession, User
from src.menus.admin.books_csv_loader import BookCSVLoaderMenu
from src.settings import WEBHOOK_ENABLE


class AdminBookMenu(OneListMenu):
    menu_name = 'admin_book_menu'

    def entry(self, update, context):
        self._load(context)
        self.send_message(context)
        if update.callback_query:
            context.bot.answer_callback_query(update.callback_query.id)
        return self.States.ACTION

    def query_objects(self, context):
        return DBSession.query(Book).all()

    def entry_points(self):
        return [CallbackQueryHandler(self.entry, pattern='^work_with_data$', pass_user_data=True)]

    def message_text(self, context, obj):
        if obj:
            message_text = f"____{'Книги'}____\n"
            message_text += "Жанр" + f": {obj.genre if obj.genre else 'Unknown'}" + '\n'
            message_text += "Название" + f": {obj.name if obj.name else 'Unknown'}" + '\n'
            message_text += "Описание" + f": {obj.description if obj.description else 'Unknown'}" + '\n'
            message_text += "Цена" + f": {obj.price if obj.price else 'Unknown'}" + '\n'
            message_text += "Картинка" + f": {'Загружена' if obj.image else 'Не загружена'}" + '\n'
            message_text += "\n"
        else:
            message_text = "Данные о книгах отсутствуют!" + '\n'

        return message_text

    def delete_ask(self, update, context):
        user = context.user_data['user']
        return super(AdminBookMenu, self).delete_ask(update, context)

    def center_buttons(self, context, obj=None):
        buttons = []
        user = context.user_data['user']
        buttons.append(InlineKeyboardButton("Добавить", callback_data="add_book"))
        if obj:
            buttons.append(InlineKeyboardButton("Редактировать", callback_data="edit_book"))
        if obj:
            buttons.append(InlineKeyboardButton("Удалить", callback_data=f"delete_{self.menu_name}"))
        return buttons

    def object_buttons(self, context, obj):
        user = context.user_data['user']
        buttons = []
        if obj:
            buttons.append(InlineKeyboardButton("Заказы", url='google.com'))
        buttons.append(InlineKeyboardButton("Импортировать данные из csv",  callback_data='import_csv'))
        return group_buttons(buttons, 1)

    def additional_states(self):
        add_books = BookAddMenu(self)
        edit_book = BookEditMenu(self)
        csv_loader = BookCSVLoaderMenu(self)
        return {
            self.States.ACTION: [add_books.handler,
                                 edit_book.handler,
                                 csv_loader.handler]
                }

    def after_delete_text(self, context):
      return "Книга удалена!"


class BookAddMenu(ArrowAddEditMenu):
    menu_name = 'books_add_menu'
    model = Book

    def entry(self, update, context):
        self._entry(update, context)
        self.load(context)
        self.send_message(context)
        return self.States.ACTION

    def query_object(self, context):
        return None

    def fields(self, context):

        fields = [self.Field('genre', "Жанр: ", validators.String(), required=True),
                  self.Field('name', "Название", validators.String(), required=True),
                  self.Field('description', "Описание", validators.String(), required=True),
                  self.Field('image', "Изображение", validators.String(), is_photo=True),
                  self.Field('price', "Цена", validators.Int(), required=True)]
        return fields

    def entry_points(self):
        return [CallbackQueryHandler(self.entry, pattern="^add_book$")]

    def save_object(self, obj, context, session=None):
        user_data = context.user_data
        obj.genre = user_data[self.menu_name]['genre']
        obj.name = user_data[self.menu_name]['name']
        obj.description = user_data[self.menu_name]['description']
        obj.image = user_data[self.menu_name]['image']
        obj.price = user_data[self.menu_name]['price']
        if not add_to_db([obj], session):
            return self.conv_fallback(context)


class BookEditMenu(ArrowAddEditMenu):
    menu_name = 'books_add_menu'
    model = Book

    def entry(self, update, context):
        self._entry(update, context)
        self.load(context)
        self.send_message(context)
        return self.States.ACTION

    def query_object(self, context):

        book = self.parent.selected_object(context)
        if book:
            return DBSession.query(Book).filter(Book.id == book.id).first()
        else:
            self.parent.update_objects(context)
            self.parent.send_message(context)
            return ConversationHandler.END

    def fields(self, context):

        fields = [self.Field('genre', "Жанр: ", validators.String(), required=True),
                  self.Field('name', "Название", validators.String(), required=True),
                  self.Field('description', "Описание", validators.String(), required=True),
                  self.Field('image', "Изображение", validators.String(), is_photo=True),
                  self.Field('price', "Цена", validators.Int(), required=True)]
        return fields

    def entry_points(self):
        return [CallbackQueryHandler(self.entry, pattern='^edit_book$')]
