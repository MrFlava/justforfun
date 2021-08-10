import enum
from botmanlib.menus.basemenu import BaseMenu
from botmanlib.menus.helpers import unknown_command, to_state, add_to_db
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, TelegramError
from telegram.ext import CallbackQueryHandler, ConversationHandler, MessageHandler, Filters, PrefixHandler

from src.models import User, DBSession
from src.menus.start.books import BooksListMenu


class StartMenu(BaseMenu):

    menu_name = 'start_menu'

    class States(enum.Enum):
        ACTION = 1

    def entry(self, update, context):
        user = DBSession.query(User).filter(User.chat_id == update.effective_user.id).first()
        if user is None and context.args:
            came_from = context.args[0]
        else:
            came_from = None

        user = self.prepare_user(User, update, context)
        user.init_permissions()
        if came_from:
            user.came_from = came_from
            add_to_db(user)

        self.clear_all_states(context)
        if self.menu_name not in context.user_data:
            context.user_data[self.menu_name] = {}

        if update.callback_query and update.callback_query.data == 'start':
            self.bot.answer_callback_query(update.callback_query.id)
            try:
                update.effective_message.edit_reply_markup()
            except (TelegramError, AttributeError):
                pass
        if not user.has_permission('start_menu_access'):
            self.bot.send_message(chat_id=user.chat_id, text="You were restricted from using this bot")
            return self.States.ACTION
        self.send_message(context)
        return self.States.ACTION

    def send_message(self, context):
         user = context.user_data['user']
         message_text = "Вас приветствует бот магаизина 'Bookstore'. Чем могу быть полезен?"
         keyboard_customer = [[InlineKeyboardButton('Список книг', callback_data='list_of_books'),
                               InlineKeyboardButton('Книжный клуб', url='https://t.me/')]]
         self.send_or_edit(context, chat_id=user.chat_id, text=message_text, reply_markup=InlineKeyboardMarkup(keyboard_customer))

    def goto_admin(self, update, context):
        context.update_queue.put(update)
        return ConversationHandler.END

    def get_handler(self):
        books_list_menu = BooksListMenu(self)
        handler = ConversationHandler(entry_points=[PrefixHandler('/', 'start', self.entry, pass_user_data=True)],
                                           states={
                                               self.States.ACTION: [books_list_menu.handler,
                                                                    MessageHandler(Filters.regex('^/admin$'), self.goto_admin),
                                                                    MessageHandler(Filters.all, to_state(self.States.ACTION))]},
                                           fallbacks=[MessageHandler(Filters.all, unknown_command(-1), pass_user_data=True)])
        return handler
