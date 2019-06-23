"""
token   - 601109474:AAF5FYt9j89otW18FPIebMqKTWtSPjVJ52M
see updates - https://api.telegram.org/bot601109474:AAF5FYt9j89otW18FPIebMqKTWtSPjVJ52M/getUpdates
admin id - 428129079
id of testing account -  772218401
"""

import telebot
from telebot.types import Message
from telebot import types
import psycopg2
import postgresql.driver as pg_driver
bot = telebot.TeleBot("601109474:AAF5FYt9j89otW18FPIebMqKTWtSPjVJ52M")
conn = psycopg2.connect(user='postgres', password='112323', host='localhost', database = 'postgres', port = 5432)
conntwo = psycopg2.connect(user='postgres', password='112323', host='localhost', database = 'postgres', port = 5432)
global count
global count_two

@bot.message_handler(commands=['start'])
def main_menu(message):
    bot.send_message(message.chat.id, "Здраствуйте, Вас приветствует бот магазина 'Bookstore'.")
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_products= types.KeyboardButton(text="Просмотреть каталог книг")
    keyboard.add(button_products)
    bot.send_message(message.chat.id,"Чем могу быть полезен?",reply_markup=keyboard )
@bot.message_handler(func=lambda mess:"Просмотреть каталог книг" == mess.text, content_types=['text'])

def watch_some_books(message):
    id = []
    title = []
    description = []
    price = []
    cursor_one = conn.cursor()
    cursor_two = conn.cursor()
    cursor_three = conn.cursor()
    cursor_four = conn.cursor()
    cursor_one.execute("SELECT num_id FROM books")
    cursor_two.execute("SELECT title FROM books")
    cursor_three.execute("SELECT description FROM books")
    cursor_four.execute("SELECT price FROM books")
    id.append(cursor_one.fetchall())
    title.append(cursor_two.fetchall())
    description.append(cursor_three.fetchall())
    price.append(cursor_four.fetchall())
    for a in id:
        bot.send_message(message.chat.id, text = a)
    for b in title:
        bot.send_message(message.chat.id, text = b)
    for c in description:
        bot.send_message(message.chat.id, text = c)
    for d in price:
        bot.send_message(message.chat.id, text = d)
@bot.message_handler(commands=['admin'])
def admin_menu(message):
    if message.from_user.id == 428129079:
        bot.send_message(message.chat.id, "Привет, админ.")
        markup_adm = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        markup_products = types.KeyboardButton(text="Продукты")
        markup_spam = types.KeyboardButton(text="Рассылка")
        markup_adm.add(markup_products,markup_spam)
        bot.send_message(message.chat.id, "С чем хочешь работать?", reply_markup=markup_adm)
    else:
        bot.send_message(message.chat.id, 'Ты не админ!')
@bot.message_handler(func=lambda mess:"Продукты" == mess.text, content_types=['text'])
def adm_products(message):
    global count
    count = 1
    markup_operations = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    add = types.KeyboardButton(text="Добавить продукт")
    delete = types.KeyboardButton(text="Удалить продукт")
    change = types.KeyboardButton(text="Изменить продукт")
    back = types.KeyboardButton(text="Вернуться")
    markup_operations.add(add,delete,change,back)
    bot.send_message(message.chat.id, "Что именно хочешь сделать?", reply_markup=markup_operations)
@bot.message_handler(func= lambda mess:"Рассылка" == mess.text, content_types=['text'])
def spam_for_adm (message):
    bot.send_message(chat_id = 428129079 , text ="Акция, купи одну книгу и получи вторую в подарок!")
    bot.send_message(chat_id = 772218401 , text ="Акция, купи одну книгу и получи вторую в подарок!")
@bot.message_handler(func= lambda mess:"Вернуться" == mess.text, content_types=['text'])
def comeback(message):
    admin_menu(message)
@bot.message_handler(func= lambda mess:"Добавить продукт" == mess.text, content_types=['text'])
def add_to_data(message):
    try:
        connthree = psycopg2.connect(user='postgres', password='112323', host='localhost', database = 'postgres', port = 5432)
        cursorr = connthree.cursor()
        cursorr.execute("INSERT INTO books (num_Id, title, description , price) VALUES (%s,%s,%s,%s)", (5, 'Книга5', 'Описание5', 300))
        count = cursorr.rowcount
        print (count, "Запись прошла успешно!")
    except (Exception, psycopg2.Error) as error :
        if(connthree):
            print("Ошибка! Что-то не так с подключением к БД. Проверьте, пожалуйста, правильно ли введены данные!", error)
@bot.message_handler(func= lambda mess:"Изменить продукт" == mess.text, content_types=['text'])
def update(message):

    request = """ UPDATE books
                SET title = %s
                WHERE num_Id = %s"""
    conn = None
    rows = 0
    try:
        connect = psycopg2.connect(user='postgres', password='112323', host='localhost', database = 'postgres', port = 5432)
        cur = connect.cursor()
        cur.execute(request, ("Книга21", 1))
        connect.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connect is not None:
            connect.close()

    return rows
@bot.message_handler(func= lambda mess:"Удалить продукт" == mess.text, content_types=['text'])
def insert_id(message):
    bot.send_message(message.chat.id, "Укажи номер(id):")
@bot.message_handler(func= lambda message: True)
def del_from_data(message):
    id_del = int(message.text)
    cursor_del = conntwo.cursor()
    cursor_del.execute("DELETE FROM books WHERE num_Id = %s", (id_del,))
bot.polling()
