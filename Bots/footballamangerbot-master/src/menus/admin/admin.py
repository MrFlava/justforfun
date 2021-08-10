import enum

from botmanlib.menus.basemenu import BaseMenu
from botmanlib.menus.helpers import group_buttons, prepare_user
from botmanlib.menus.ready_to_use.permissions import PermissionsMenu
from botmanlib.messages import send_or_edit, delete_interface, delete_user_message
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, Filters, MessageHandler, CallbackQueryHandler, PrefixHandler

from src.menus.admin.teams import TeamsMenu
from src.models import User, Permission


class AdminMenu(BaseMenu):
    menu_name = 'admin_menu'

    class States(enum.Enum):
        ACTION = 1

    def entry(self, update, context):
        user = prepare_user(User, update, context)
        _ = context.user_data['user'].translator

        if not user.has_permission('admin_menu_access'):
            return ConversationHandler.END

        if self.menu_name not in context.user_data:
            context.user_data[self.menu_name] = {}

        delete_interface(context)
        self.send_message(context)

        if update.callback_query:
            self.bot.answer_callback_query(update.callback_query.id)

        return self.States.ACTION

    def send_message(self, context):
        user = context.user_data['user']
        buttons = []

        if user.has_permission('permissions_menu_access'):
            buttons.append(InlineKeyboardButton("Права", callback_data='permissions'))

        buttons.append(InlineKeyboardButton("Футбольные клубы Украины", callback_data='football_clubs'))

        buttons.append(InlineKeyboardButton("Вернуться в главное меню", callback_data='start'))

        send_or_edit(context, chat_id=user.chat_id, text="Админ-меню:", reply_markup=InlineKeyboardMarkup(group_buttons(buttons, 1)))

    def goto_next_menu(self, update, context):
        context.update_queue.put(update)
        return ConversationHandler.END

    def get_handler(self):
        teams_menu = TeamsMenu(self)
        permissions_menu = PermissionsMenu(User, Permission, parent=self)

        handler = ConversationHandler(entry_points=[PrefixHandler('/', "admin", self.entry)],
                                      states={
                                          self.States.ACTION: [
                                                               CallbackQueryHandler(self.entry, pattern='^back$'),
                                                               permissions_menu.handler,
                                                               teams_menu.handler],

                                      },
                                      fallbacks=[
                                          MessageHandler(Filters.regex('^/start$'), self.goto_next_menu),
                                          MessageHandler(Filters.all, lambda update, context: delete_user_message(update))],
                                      allow_reentry=True)

        return handler
