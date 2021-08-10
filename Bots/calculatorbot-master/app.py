import math
import logging
import telegram
import threading
import formencode
from local_settings import Token
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, ConversationHandler, RegexHandler, Filters
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
reply_keyboard = [['/calc','/end']]
markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
def start(bot, update):
    update.message.reply_text('Здравствуйте! Я бот-калькулятор.Для начала нажмите на одну из команд (/calc - для просмотра доступных операций /end -для окончания работы с ботом). ',reply_markup = markup)
   
def basic_menu(bot, update):
    keyboard_customer = [[InlineKeyboardButton('Узнать сумму', callback_data='узнать сумму'),InlineKeyboardButton('Узнать разность', callback_data= 'узнать разность')],[InlineKeyboardButton('Узнать произведение', callback_data= 'узнать произведение'),InlineKeyboardButton('Узнать частное', callback_data= 'узнать частное')]]
    reply_markup = InlineKeyboardMarkup(keyboard_customer)
    update.message.reply_text('Выберите одну из доступных операций.', reply_markup = reply_markup)
def shutdown():
     updater.stop()
     updater.is_idle = False
def end(bot, update):
    threading.Thread(target=shutdown).start()
def selected_operation(bot,update,user_data):
        query = update.callback_query
        user_data['operation'] = query.data
        if user_data['operation'] == 'узнать сумму':
            bot.send_message(text="Хорошо, вы выбрали операцию: {} . Сначала введите   /sum (значение) , затем повторите эту операцию .".format(query.data),chat_id=query.message.chat_id,message_id=query.message.message_id)
        elif user_data['operation'] == 'узнать разность':
            bot.send_message(text="Хорошо, вы выбрали операцию: {} . Сначала введите   /razn (значение) , затем повторите эту операцию .".format(query.data),chat_id=query.message.chat_id,message_id=query.message.message_id)
        elif user_data['operation'] == 'узнать произведение':
            bot.send_message(text="Хорошо, вы выбрали операцию: {} . Сначала введите   /umnoz (значение) , затем повторите эту операцию .".format(query.data),chat_id=query.message.chat_id,message_id=query.message.message_id)
        elif user_data['operation'] == 'узнать частное':
            bot.send_message(text="Хорошо, вы выбрали операцию: {} . Сначала введите   /del (значение) , затем повторите эту операцию .".format(query.data),chat_id=query.message.chat_id,message_id=query.message.message_id)

def get_sum(bot,update, user_data):
    text = update.message.text.replace('/sum','')
    text = "".join(text.split())
    if 'a' not in user_data:
        val = formencode.validators.Number()
        user_data['a'] = val.to_python(text)
    elif 'b' not in user_data:
        val = formencode.validators.Number()
        user_data['b'] = val.to_python(text)
        message_sum = f"a + b = {user_data['a']+ user_data['b']}"
        bot.send_message(chat_id=update.effective_user.id, text=message_sum)
        del user_data['a']
        del user_data['b']
def get_razn(bot,update,user_data):
    text = update.message.text.replace('/razn','')
    text = "".join(text.split())
    if 'a' not in user_data:
        val = formencode.validators.Number()
        user_data['a'] = val.to_python(text)
    elif 'b' not in user_data:
        val = formencode.validators.Number()
        user_data['b'] = val.to_python(text)
        message_min = f"a - b = {user_data['a']- user_data['b']}"
        bot.send_message(chat_id=update.effective_user.id, text=message_min)
        del user_data['a']
        del user_data['b']
def get_multiply(bot,update,user_data):
    text = update.message.text.replace('/umnoz','')
    text = "".join(text.split())
    if 'a' not in user_data:
        val = formencode.validators.Number()
        user_data['a'] = val.to_python(text)
    elif 'b' not in user_data:
        val = formencode.validators.Number()
        user_data['b'] = val.to_python(text)
        message_del = f"a / b = {user_data['a']/ user_data['b']}"
        bot.send_message(chat_id=update.effective_user.id, text=message_del)
        del user_data['a']
        del user_data['b']
def  get_division(bot,update,user_data):
    text = update.message.text.replace('/del','')
    text = "".join(text.split())
    if 'a' not in user_data:
        val = formencode.validators.Number()
        user_data['a'] = val.to_python(text)
    elif 'b' not in user_data:
        val = formencode.validators.Number()
        user_data['b'] = val.to_python(text)
        message_um = f"a x b = {user_data['a']* user_data['b']}"
        bot.send_message(chat_id=update.effective_user.id, text=message_um)
        del user_data['a']
        del user_data['b']
updater = Updater(Token)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("calc", basic_menu))
dp.add_handler(CommandHandler("end", end))
dp.add_handler(CommandHandler("sum", get_sum, pass_user_data=True))
dp.add_handler(CommandHandler("razn", get_razn, pass_user_data=True))
dp.add_handler(CommandHandler("umnoz", get_multiply, pass_user_data=True))
dp.add_handler(CommandHandler("del", get_division, pass_user_data=True))
MessageHandler(Filters.text, get_sum, pass_user_data=True)
MessageHandler(Filters.text, get_razn, pass_user_data=True)
MessageHandler(Filters.text, get_multiply, pass_user_data=True)
MessageHandler(Filters.text, get_division, pass_user_data=True)
dp.add_handler(CallbackQueryHandler(selected_operation, pass_user_data=True))

updater.start_polling()
updater.idle()
