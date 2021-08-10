
from botmanlib.menus import OneListMenu
from telegram.ext import CallbackQueryHandler
from src.models import DBSession, Game


class UserTeamGamesMenu(OneListMenu):
    menu_name = 'team_games_menu'
    model = Game

    def entry(self, update, context):
        return super(UserTeamGamesMenu, self).entry(update, context)

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

    def additional_states(self):

        return {self.States.ACTION: []}


