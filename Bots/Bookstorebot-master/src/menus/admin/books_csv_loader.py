import csv
import enum
from io import StringIO

import requests
from botmanlib.menus import BaseMenu
from botmanlib.menus.helpers import to_state, unknown_command, require_permission
from formencode import validators, Invalid
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, CallbackQueryHandler, MessageHandler, Filters

from src.models import DBSession, Book


class BookCSVLoaderMenu(BaseMenu):

    menu_name = 'book_csv_loader_menu'

    class States(enum.Enum):
        CSV_WAIT = 1
        END = 2

    def entry(self, update, context):
        user = context.user_data['user']

        if self.menu_name not in context.user_data:
            context.user_data[self.menu_name] = {}

        self.send_message(context)
        return self.States.CSV_WAIT

    def send_message(self, context):
        user = context.user_data['user']
        message_text = "Отправьте мне csv файл."
        buttons = [[InlineKeyboardButton("Назад", callback_data='back_from_csv')]]
        self.send_or_edit(context, chat_id=user.chat_id, text=message_text, reply_markup=InlineKeyboardMarkup(buttons))

    def back(self, update, context):
        self.parent.update_objects(context)
        self.parent.send_message(context)
        return ConversationHandler.END

    def load_csv_file(self, update, context):
        user = context.user_data['user']
        _ = context.user_data["_"]
        file = StringIO(update.message.document.get_file().download_as_bytearray().decode("utf-8"))
        categories = DBSession.query(Book).all()
        dr = csv.DictReader(file)
        data = []
        errors = []
        image_validator = validators.URL()
        integer_validator = validators.Int()
        for idx, row in enumerate(dr):
            idx += 1
            row_data = {'id': None,
                        'genre': None,
                        'name': None,
                        'description': None,
                        'price': None,
                        'image': None
                        }
            for key in row:
                if key.lower() == 'id' or key.lower() == "":
                    try:
                        value = integer_validator.to_python(row[key])
                        row_data['id'] = value
                    except Invalid:
                        errors.append({'row': idx + 1, 'column': key, 'message': "Value must be integer number"})

                elif key.lower() == "genre":
                    row_data['genre'] = row[key]

                elif key.lower() == "name":
                    row_data['name'] = row[key]

                elif key.lower() == "description":
                    row_data['description'] = row[key]

                elif key.lower() == "price":
                    try:
                        value = integer_validator.to_python(row[key])
                        row_data['price'] = value
                    except Invalid:
                        errors.append({'row': idx + 1, 'column': key, 'message': "Value must be integer number"})
                elif key.lower().startswith("image"):
                    row_data['image'] = row[key]

            if row_data.get('image', False):
                link = row_data['image']
                try:
                    value = image_validator.to_python(link)
                    if not value:
                        errors.append({'row': idx + 1, 'column': 'image', 'message': "Wrong image link"})
                        continue
                    res = requests.get(value)
                    if res.status_code != 200:
                        errors.append({'row': idx + 1, 'column': 'image', 'message': "Wrong image link"})
                except Invalid:
                    errors.append({'row': idx + 1, 'column': 'image', 'message': "Wrong image link"})

            if 'id' not in row_data:
                errors.append({'row': idx + 1, 'column': "ID", 'message': "ID value is required"})

            if 'genre' not in row_data:
                errors.append({'row': idx + 1, 'column': "genre", 'message': "genre value is required"})

            if 'name' not in row_data:
                errors.append({'row': idx + 1, 'column': "name", 'message': "name value is required"})

            if 'description' not in row_data:
                errors.append({'row': idx + 1, 'column': "description", 'message': "description value is required"})

            if 'price' not in row_data:
                errors.append({'row': idx + 1, 'column': "price", 'message': "price value is required"})

            if not errors:
                data.append(row_data)

            buttons = [[InlineKeyboardButton(_("Назад"), callback_data='back_from_csv')]]
            self.delete_interface(context)

            if errors:
                message_text = str(len(errors)) + ' ' + _("errors occurred while importing file:") + '\n'
                for idx, error in enumerate(errors):
                    message_text += f'{idx + 1}. {_("Row")} №{error["row"]}, '
                    message_text += f'{_("Column")} {error["column"]}, ' if error['column'] else ""
                    message_text += error['message'] + '\n'

                message_text += '\n' + _("Пожалуйста, отправьте мне CSV файл.")
                self.send_or_edit(context, chat_id=user.chat_id, text=message_text, reply_markup=InlineKeyboardMarkup(buttons))

            else:
                for row_data in data:
                    obj = DBSession.query(Book).filter(Book.id == row_data['id']).first()
                    if obj is None:
                        obj = Book()
                    obj.id = row_data['id']
                    obj.genre = row_data['genre']
                    obj.name = row_data['name']
                    obj.description = row_data['description']
                    obj.price = row_data['price']
                    image_link = row_data.get('image', None)
                    if image_link:
                        mes = self.bot.send_photo(chat_id=user.chat_id, photo=image_link)
                        obj.image = mes.photo[-1].file_id
                        mes.delete()
                    DBSession.add(obj)
                DBSession.commit()
                self.send_or_edit(context, chat_id=user.chat_id, text="Данные импортировались успешно", reply_markup=InlineKeyboardMarkup(buttons))
            return self.States.CSV_WAIT

    def get_handler(self):
            handler = ConversationHandler(entry_points=[CallbackQueryHandler(self.entry, pattern='^import_csv$')],
                                      states={
                                          self.States.CSV_WAIT: [CallbackQueryHandler(self.back, pattern="^back_from_csv$"),
                                                                 MessageHandler(Filters.document.mime_type('text/csv'), self.load_csv_file),
                                                                 MessageHandler(Filters.all, to_state(self.States.CSV_WAIT))],
                                          self.States.END: [CallbackQueryHandler(self.back, pattern="^back_from_csv$"),
                                                            MessageHandler(Filters.all, to_state(self.States.END))]
                                      },
                                      fallbacks=[MessageHandler(Filters.all, unknown_command(-1))],
                                      allow_reentry=True)
            return handler
