import enum

from botmanlib.menus.basemenu import BaseMenu
from botmanlib.menus.helpers import prepare_user
from botmanlib.messages import send_or_edit, delete_interface, delete_user_message
from telegram import TelegramError, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, CallbackQueryHandler, Filters, MessageHandler, PrefixHandler

from src.models import User
from src.menus.start.teams import TeamMenu


class StartMenu(BaseMenu):
    menu_name = 'start_menu'

    class States(enum.Enum):
        ACTION = 1

    def entry(self, update, context):
        user = prepare_user(User, update, context)
        _ = user.translator

        if self.menu_name not in context.user_data:
            context.user_data[self.menu_name] = {}

        if update.effective_message and update.effective_message.text and update.effective_message.text.startswith("/"):
            delete_interface(context)

        if update.callback_query and update.callback_query.data == 'start':
            update.callback_query.answer()
            try:
                update.effective_message.edit_reply_markup()
            except (TelegramError, AttributeError):
                pass

        if not user.has_permission('start_menu_access'):
            self.bot.send_message(chat_id=user.chat_id, text=_("You were restricted from using this bot"))
            return self.States.ACTION

        self.send_message(context)
        return self.States.ACTION

    def send_message(self, context):
        user = context.user_data['user']
        _ = user.translator
        buttons = [[InlineKeyboardButton("Футбольные клубы Украины", callback_data='football_clubs')]]

        message_text = "Приветствую, я 'Football manager bot' !"

        send_or_edit(context, chat_id=user.chat_id, text=message_text, reply_markup=InlineKeyboardMarkup(buttons))
        return self.States.ACTION

    def goto_next_menu(self, update, context):
        context.update_queue.put(update)
        return ConversationHandler.END

    def get_handler(self):
        team_menu = TeamMenu(self)
        handler = ConversationHandler(entry_points=[PrefixHandler('/', 'start', self.entry),
                                                    CallbackQueryHandler(self.entry, pattern='^start$')],
                                      states={
                                          self.States.ACTION: [PrefixHandler('/', 'admin', self.goto_next_menu),
                                                               team_menu.handler]},
                                      fallbacks=[
                                                 MessageHandler(Filters.all, lambda update, context: delete_user_message(update))],
                                      allow_reentry=True)

        return handler
