
from botmanlib.menus import OneListMenu, ArrowAddEditMenu
from botmanlib.menus.helpers import add_to_db

from formencode import validators
from telegram import InlineKeyboardButton
from telegram.ext import CallbackQueryHandler, ConversationHandler


from src.models import DBSession, Game, Enemy


class TeamGamesMenu(OneListMenu):
    menu_name = 'team_games_menu'
    model = Game

    def entry(self, update, context):
        return super(TeamGamesMenu, self).entry(update, context)

    def query_objects(self, context):
        team = self.parent.selected_object(context)
        return DBSession.query(Game).filter(Game.team_id == team.id).all()

    def entry_points(self):
        return [CallbackQueryHandler(self.entry, pattern='^games$', pass_user_data=True)]

    def message_text(self, context, obj):

        if obj:
            message_text = "Игры с зарубежными командами" + '\n'
            for enemy in obj.enemies:
                message_text += f"Название команды противника: {enemy.name}" + '\n'
                message_text += f"Страна: {enemy.country}" + '\n'
                message_text += f"Старший тренер: {enemy.senior_coach}" + '\n'
            message_text += '\n'
            message_text += f"Дата проведения: {obj.date.strftime('%d.%m.%Y ')}" + '\n'
            message_text += f"Кол-во пропущенных мячей: {obj.goals_conceded_quantity}" + '\n'
            message_text += f"Кол-во забитых мячей: {obj.goals_scored_quantity}" + '\n'
        else:
            message_text = "Нет никаих данных о играх с зарубежными командами!"

        return message_text

    def center_buttons(self, context, o=None):
        buttons = []
        buttons.append(InlineKeyboardButton("Добавить инофрмацию о игре", callback_data="add_game_data"))
        if o:
            buttons.append(InlineKeyboardButton("Редактировать инофрмацию о игре", callback_data="edit_game_data"))
        return buttons

    def additional_states(self):
        add_game = AddGameMenu(self)
        edit_game = EditGameMenu(self)
        return {self.States.ACTION: [add_game.handler,
                                     edit_game.handler]}


class AddGameMenu(ArrowAddEditMenu):
    menu_name = 'add_game_menu'
    model = Game

    def entry(self, update, context):
        return super(AddGameMenu, self).entry(update, context)

    def query_object(self, context):
        return None

    def fields(self, context):
        fields = [
                   self.Field('name', "*Название команды противника", validators.String(), required=True),
                   self.Field('country', "*Страна", validators.String(), required=True),
                   self.Field('senior_coach', "*Старший тренер", validators.String(), required=True),
                   self.Field('date', "Дата проведения", validators.DateConverter()),
                   self.Field('goals_conceded_quantity', "Кол-во пропущенных мячей", validators.Number()),
                   self.Field('goals_scored_quantity', "Кол-во забитых мячей", validators.Number())]
        return fields

    def entry_points(self):
        return [CallbackQueryHandler(self.entry, pattern="^add_game_data$")]

    def save_object(self, obj, context, session=None):
        user_data = context.user_data
        game = Game()
        enemy = Enemy()
        enemy.name = user_data[self.menu_name]['name']
        enemy.country = user_data[self.menu_name]['country']
        enemy.senior_coach = user_data[self.menu_name]['senior_coach']
        game.enemies.append(enemy)
        game.goals_conceded_quantity = user_data[self.menu_name]['goals_conceded_quantity']
        game.goals_scored_quantity = user_data[self.menu_name]['goals_scored_quantity']
        game.date = user_data[self.menu_name]['date']
        game.team = self.parent.parent.selected_object(context)
        if not add_to_db([game, enemy], session):
            return self.conv_fallback(context)


class EditGameMenu(ArrowAddEditMenu):
    menu_name = 'edit_game_menu'
    model = Game

    def entry(self, update, context):
        return super(EditGameMenu, self).entry(update, context)

    def query_object(self, context):

        game = self.parent.selected_object(context)
        if game:
            return DBSession.query(Game).filter(Game.id == game.id).first()
        else:
            self.parent.update_objects(context)
            self.parent.send_message(context)
            return ConversationHandler.END

    def fields(self, context):
        fields = [
                   self.Field('name', "*Название команды противника", validators.String(), required=True),
                   self.Field('country', "*Страна", validators.String(), required=True),
                   self.Field('senior_coach', "*Старший тренер", validators.String(), required=True),
                   self.Field('date', "Дата проведения", validators.DateConverter()),
                   self.Field('goals_conceded_quantity', "Кол-во пропущенных мячей", validators.Number()),
                   self.Field('goals_scored_quantity', "Кол-во забитых мячей", validators.Number())]
        return fields

    def entry_points(self):
        return [CallbackQueryHandler(self.entry, pattern="^edit_game_data$")]

    def save_object(self, obj, context, session=None):
        user_data = context.user_data
        enemy = Enemy()
        enemy.name = user_data[self.menu_name]['name']
        enemy.country = user_data[self.menu_name]['country']
        enemy.senior_coach = user_data[self.menu_name]['senior_coach']
        obj.enemies.append(enemy)
        obj.goals_conceded_quantity = user_data[self.menu_name]['goals_conceded_quantity']
        obj.goals_scored_quantity = user_data[self.menu_name]['goals_scored_quantity']
        obj.date = user_data[self.menu_name]['date']

        if not add_to_db([obj, enemy], session):
            return self.conv_fallback(context)
