"""

https://api.telegram.org/bot757283759:AAENGob365hUYh9DxpVleFlKC4a1uwgkkzY/getUpdates
token for old bot = 757283759:AAENGob365hUYh9DxpVleFlKC4a1uwgkkzY

"""
import telebot
from telebot.types import Message
from telebot import types
bot = telebot.TeleBot("512843194:AAGr6vDcVELIX2hqLpW8Vz5KgkBMhlJNAaU")

global count

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "По всем вопросам - @m8_uwot")
@bot.message_handler(commands=['start'])
def send_group(message):
    markup_group = types.ReplyKeyboardMarkup()
    markup_group.row('035-17-1', '035-17-2')
    markup_group.row('035-17-3', '035-17-4')
    bot.send_message(message.chat.id, "Выбери свою группу:", reply_markup=markup_group)
@bot.message_handler(func=lambda mess:"035-17-1" == mess.text, content_types=['text'])
def set_days(message):
    global count
    count = 1
    markup_day = types.ReplyKeyboardMarkup()
    markup_day.row('Понедельник','Вторник')
    markup_day.row('Среда','Четверг')
    markup_day.row('Пятница','Назад')
    bot.send_message(message.chat.id, "Выбери день недели:",reply_markup=markup_day)
@bot.message_handler(func=lambda mess:"035-17-2" == mess.text, content_types=['text'])
def set_daystwo(message):
    global count
    count = 2
    markup_day = types.ReplyKeyboardMarkup()
    markup_day.row('Понедельник','Вторник')
    markup_day.row('Среда','Четверг')
    markup_day.row('Пятница','Назад')
    bot.send_message(message.chat.id, "Выбери день недели:",reply_markup=markup_day)
@bot.message_handler(func=lambda mess:"035-17-3"== mess.text, content_types=['text'])
def set_daythree(message):
    global count
    count = 3
    markup_day = types.ReplyKeyboardMarkup()
    markup_day.row('Понедельник','Вторник')
    markup_day.row('Среда','Четверг')
    markup_day.row('Пятница','Назад')
    bot.send_message(message.chat.id, "Выбери день недели:",reply_markup=markup_day)
@bot.message_handler(func=lambda mess:"035-17-4"== mess.text, content_types=['text'])
def set_daysfour(message):
    global count
    count = 4
    markup_day = types.ReplyKeyboardMarkup()
    markup_day.row('Понедельник','Вторник')
    markup_day.row('Среда','Четверг')
    markup_day.row('Пятница','Назад')
    bot.send_message(message.chat.id, "Выбери день недели:",reply_markup=markup_day)
@bot.message_handler(func=lambda mess:"Назад" == mess.text, content_types=['text'])
def comeback(message):
    send_group(message)
@bot.message_handler(func = lambda mess:"Понедельник" == mess.text, content_types=['text'])
def bloody_monday(message):
    if count == 1:
        bot.send_message(message.chat.id," 2.ПКА Черкащенко 3. ПКН Галушко")
    elif count == 2:
        bot.send_message(message.chat.id," 2.ПКН Хуртак 3.ППА Черкащенко")
    elif count == 3:
        bot.send_message(message.chat.id, "3. ПКН Хуртак")
    elif count == 4:
        bot.send_message(message.chat.id,"2.ПКА Высоцкая 3.ПКА Высоцкая")
@bot.message_handler(func = lambda mess:"Вторник" == mess.text, content_types=['text'])
def tuesday(message):
    if count == 1:
        bot.send_message(message.chat.id, "3. ИАМ Черкащенко/АДМС Столярская 4.ПКН Галушко 5. Физкультура")
    elif count == 2:
        bot.send_message(message.chat.id, "3. ИАМ Черкащенко/АДМС Столярская 4. ПКН Хуртак 5. Физкультура")
    elif count == 3:
        bot.send_message(message.chat.id, "3. ПЛАУМ Нестерова 4.ППА Черкащенко 5. Физкультура")
    elif count == 4:
        bot.send_message(message.chat.id, "3. ПЛАУМ Нестерова 4.ППА Щуров 5.Физкультура")
@bot.message_handler(func = lambda mess:"Среда" == mess.text, content_types=['text'])
def wednesday(message):
    if count == 1:
        bot.send_message(message.chat.id, "2. История англ. Черкащенко/История англ. Черкащенко 3.ПКА Черкащенко 4.ПЛАУМ Нестерова/ПЛАУМ Нестерова")
    elif count == 2:
        bot.send_message(message.chat.id, "2. История англ. Черкащенко/История англ. Черкащенко 3.ПКА Введенская 4. ПЛАУМ Нестерова/ПЛАУМ Нестерова")
    elif count == 3:
        bot.send_message(message.chat.id, "2. -/История англ. Черкащенко 3.ПКА Бойко 4.ПЛАУМ Нестерова")
    elif count == 4:
        bot.send_message(message.chat.id, "3.ПКН Короткова 4.ПЛАУМ Нестерова")
@bot.message_handler(func = lambda mess:"Четверг" == mess.text, content_types=['text'])
def thursday(message):
        if count == 1:
            bot.send_message(message.chat.id, "2. АДМС Столярская 3.ППА Орел 4.ППА Орел/СУК Щелкунов 5.СУК Щелкунов/ПЛАУМ Нестерова")
        elif count == 2:
            bot.send_message(message.chat.id, "2.АДМС Столярская  3.ППА Орел 4.ППА Орел/СУК Щелкунов 5.СУК Щелкунов/ПЛАУМ Нестерова")
        elif count == 3:
            bot.send_message(message.chat.id, "2.ПКА Бойко 3.ППА Черкащенко 4.АДМС Столярская/СУК Щелкунов 5.-/СУК Щелкунов")
        elif count == 4:
            bot.send_message(message.chat.id, "4. АДМС Столярская/СУК Щелкунов 5.-/СУК Щелкунов")
@bot.message_handler(func = lambda mess:"Пятница" == mess.text, content_types=['text'])
def otdix_in_friday(message):
    if count == 1:
        bot.send_message(message.chat.id, "Никаких пар нет")
    elif count == 2:
        bot.send_message(message.chat.id, "Никаких пар нет")
    elif count == 3:
        bot.send_message(message.chat.id, "Никаких пар нет")
    elif count == 4:
        bot.send_message(message.chat.id, "Никаких пар нет")

bot.polling()
