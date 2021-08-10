import enum

from botmanlib.models import Database, BaseUser, UserPermissionsMixin, BasePermission, BaseUserSession, UserSessionsMixin, ModelPermissionsBase
from sqlalchemy import Column, String, ForeignKey, Integer, Enum, DateTime
from sqlalchemy.orm import relationship, object_session


database = Database()
Base = database.Base


class User(Base, BaseUser, UserPermissionsMixin, UserSessionsMixin):
    __tablename__ = 'users'

    def init_permissions(self):
        session = object_session(self)
        if session is None:
            session = database.DBSession
        for permission in ['start_menu_access',
                           ]:
            perm = session.query(Permission).get(permission)
            if perm not in self.permissions:
                self.permissions.append(perm)


class Permission(BasePermission, Base):
    __tablename__ = 'permissions'


class UserSession(BaseUserSession, Base):
    __tablename__ = 'user_sessions'


class TeamLeague(enum.Enum):
    highest = 'highest'
    first = 'first'
    second = 'second'
    third = 'third'


class PlayerViolations(enum.Enum):
    free_kick = 'Free kick'
    penalty = 'Penalty'
    yellow_card = 'Yellow card'
    red_card = 'Red card'


class PlayerPosition(enum.Enum):
    goalkeeper = 'Goalkeeper'
    defender = 'Defender'
    midfielder = 'Midfielder'
    attack = 'Attack'
    captain = 'Captain'
    reserve_player = 'Reserve player'


class PlayerGame(Base):
    __tablename__ = 'player_game_association_table'

    player_id = Column(Integer, ForeignKey('players.id'), primary_key=True)
    player = relationship("Player")
    game_id = Column(Integer, ForeignKey('games.id'), primary_key=True)
    game = relationship("Game")

    cash_bonus = Column(Integer, default=0)
    player_violations = Column(Enum(PlayerViolations))

    def player_violations_str(self):
        if self.player_violations is PlayerViolations.free_kick:
            player_violations = "Штрафной удар"
        elif self.player_violations is PlayerViolations.penalty:
            player_violations = "Пенальти"
        elif self.player_violations is PlayerViolations.yellow_card:
            player_violations = "Желтая карточка"
        elif self.player_violations is PlayerViolations.red_card:
            player_violations = "Красная карточка"
        else:
            player_violations = "Нет нарушений"
        return player_violations


class Team(Base, ModelPermissionsBase):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    since = Column(Integer, nullable=False)
    league = Column(Enum(TeamLeague), default=TeamLeague.third)
    manager_FIO = Column(String, nullable=False)
    contact_number = Column(String, nullable=False)

    players = relationship("Player", back_populates='team', cascade='all ,delete')
    games = relationship("Game", back_populates='team', cascade='all, delete')

    def league_str(self):

        if self.league is TeamLeague.third:
            league = "Третья лига"
        elif self.league is TeamLeague.second:
            league = "Вторая лига"
        elif self.league is TeamLeague.first:
            league = "Первая лига"
        elif self.league is TeamLeague.highest:
            league = "Высшая лига"
        else:
            league = "Неизвестно"
        return league


class Player(Base, ModelPermissionsBase):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    FIO = Column(String, nullable=False)
    position = Column(Enum(PlayerPosition), default=PlayerPosition.reserve_player)
    date_of_birth = Column(DateTime, nullable=False)
    in_team_since = Column(Integer, nullable=False)
    contract_value = Column(Integer, nullable=False)

    def position_str(self):

        if self.position is PlayerPosition.reserve_player:
            position = "На замене"
        elif self.position is PlayerPosition.goalkeeper:
            position = "Вратарь"
        elif self.position is PlayerPosition.attack:
            position = "Атакующий"
        elif self.position is PlayerPosition.captain:
            position = "Капитан"
        elif self.position is PlayerPosition.defender:
            position = "Защитник"
        elif self.position is PlayerPosition.midfielder:
            position = "Полузащитник"
        else:
            position = "Неизвестно"
        return position

    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    team = relationship("Team", back_populates="players")
    games = relationship("Game", secondary=PlayerGame.__table__, back_populates="players", lazy='joined')


class Game(Base, ModelPermissionsBase):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    goals_conceded_quantity = Column(Integer, default=0)
    goals_scored_quantity = Column(Integer, default=0)

    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    team = relationship("Team", back_populates="games")
    enemies = relationship("Enemy", back_populates='game', cascade='all ,delete')
    players = relationship("Player", secondary=PlayerGame.__table__, lazy='joined')


class Enemy(Base, ModelPermissionsBase):
    __tablename__ = 'enemies'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    senior_coach = Column(String, nullable=False)

    game_id = Column(Integer, ForeignKey('games.id'), nullable=False)
    game = relationship("Game", back_populates="enemies")


DBSession = database.DBSession
GameSession = database.sessionmaker()
