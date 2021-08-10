import os
import csv
import enum

from botmanlib.menus.basemenu import BaseMenu
from botmanlib.menus.helpers import add_to_db, unknown_command, to_state, group_buttons
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler, Filters, MessageHandler, CallbackQueryHandler
from src.settings import MEDIA_FOLDER

from src.menus.admin.book_functions import AdminBookMenu
from src.models import DBSession, User, Permission


class AdminMenu(BaseMenu):

    menu_name = 'admin_menu'

    class States(enum.Enum):
        ACTION = 1
        ABOUT_ADMIN = 2
        DOWNLOAD_USERS = 3

    def entry(self, update, context):

        user = self.prepare_user(User, update, context)
        if not user.has_permission('admin_menu_access'):
            return ConversationHandler.END

        if self.menu_name not in context.user_data:
            context.user_data[self.menu_name] = {}

        self.delete_interface(context)
        self.send_message(context)

        if update.callback_query:
            self.bot.answer_callback_query(update.callback_query.id)

        return self.States.ACTION

    def send_message(self, context):
        user = context.user_data['user']
        buttons = []

        buttons.append(InlineKeyboardButton("Работа с данными", callback_data='work_with_data'))
        buttons.append(InlineKeyboardButton("О админ-моде", callback_data='about_admin_mode'))
        buttons.append(InlineKeyboardButton("Получить данные о пользователях", callback_data='import_users_data'))
        buttons.append(InlineKeyboardButton("Вернуться к главному меню", callback_data='goto_start'))

        return self.send_or_edit(context, chat_id=user.chat_id, text="Админ-меню", reply_markup=InlineKeyboardMarkup(group_buttons(buttons, 1)))

    def about_admin(self, update, context):
        buttons = [[InlineKeyboardButton("Назад", callback_data='back_to_admin')]]
        self.send_or_edit(context, chat_id=context.user_data['user'].chat_id, text='Режим администратора позволяет работать с данными', reply_markup=InlineKeyboardMarkup(buttons))
        return self.States.ABOUT_ADMIN

    def goto_start(self, update, context):
        self.delete_interface(context)
        update.callback_query.data = 'start'
        context.update_queue.put(update)
        return ConversationHandler.END

    def export_users(self, update, context):
        user = context.user_data['user']

        users = DBSession.query(User).all()

        with open(os.path.join(MEDIA_FOLDER, 'users.csv'), 'w') as writeFile:
            writer = csv.DictWriter(writeFile, ["id", "First name", "Last name", "Username", "Language code", "Active", "Join date"])
            writer.writeheader()
            for _user in users:
                writer.writerow(
                    {'id': _user.chat_id, 'First name': _user.first_name, 'Last name': _user.last_name, 'Username': _user.username,
                     'Language code': _user.language_code, 'Active': _user.active,
                     'Join date': _user.join_date})

        with open(os.path.join(MEDIA_FOLDER, 'users.csv'), 'rb') as file:
            button = InlineKeyboardButton("Назад", callback_data='back')
            context.bot.send_document(chat_id=user.chat_id, document=file, reply_markup=InlineKeyboardMarkup([[button]]))
        return self.States.DOWNLOAD_USERS

    def back_to_admin(self, update, context):
        self.send_message(context)
        return self.States.ACTION

    def get_handler(self):
        book_menu = AdminBookMenu(self)

        handler = ConversationHandler(entry_points=[MessageHandler(Filters.regex('^/admin$'), self.entry)],
                                      states={
                                          AdminMenu.States.ACTION: [book_menu.handler,

                                                                    CallbackQueryHandler(self.entry, pattern='^back$'),
                                                                    CallbackQueryHandler(self.goto_start, pattern='^goto_start$'),
                                                                    CallbackQueryHandler(self.about_admin, pattern='^about_admin_mode$'),
                                                                    CallbackQueryHandler(self.export_users, pattern='^import_users_data$'),
                                                                    MessageHandler(Filters.regex('^/start$'), self.goto_start),book_menu.handler,
                                                                    MessageHandler(Filters.all, to_state(AdminMenu.States.ACTION))],
                                          AdminMenu.States.ABOUT_ADMIN: [CallbackQueryHandler(self.back_to_admin, pattern='^back_to_admin$'),
                                                                         MessageHandler(Filters.all, to_state(self.States.ABOUT_ADMIN))],
                                          AdminMenu.States.DOWNLOAD_USERS: [CallbackQueryHandler(self.entry, pattern='^back$'),
                                                                            MessageHandler(Filters.all, to_state(AdminMenu.States.DOWNLOAD_USERS))]

                                      },
                                      fallbacks=[MessageHandler(Filters.all, unknown_command(-1))],
                                      allow_reentry=True)
        return handler


