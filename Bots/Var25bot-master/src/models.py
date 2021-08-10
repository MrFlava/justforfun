import enum

from botmanlib.models import Database, BaseUser, UserPermissionsMixin, BasePermission, BaseUserSession, UserSessionsMixin
from sqlalchemy import Column,  Integer, Enum, String, ForeignKey, DateTime
from sqlalchemy.orm import object_session, relationship

database = Database()
Base = database.Base


class SocialPosition(enum.Enum):
    employee = 'employee'
    student = 'student'
    businessman = 'businessman'
    pensioner = 'pensioner'
    working = 'working'

    def to_str(self):
        if self is SocialPosition.employee:
            return "Служащий"
        elif self is SocialPosition.student:
            return "Учащийся"
        elif self is SocialPosition.businessman:
            return "Предприниматель"
        elif self is SocialPosition.pensioner:
            return "Пенсионер"
        elif self is SocialPosition.working:
            return "Рабочий"
        else:
            return "Неизвестно"


class DogCompetitions(Base):
    __tablename__ = 'dog_competitions_association_table'

    dog_id = Column(Integer, ForeignKey('dogs.id'), primary_key=True)
    dog = relationship("Dog")
    competition_id = Column(Integer, ForeignKey('competitions.id'), primary_key=True)
    competition = relationship("Competition")
    reward = Column(Integer, default=0)


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


class DogTrainingClub(Base):
    __tablename__ = 'dogs_training_club'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    district = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    entrance_fee = Column(Integer, nullable=False)

    dogs = relationship("Dog", back_populates='dog_training_club', cascade='all ,delete')
    competitions = relationship("Competition", back_populates='club', cascade='all, delete')


class Dog(Base):
    __tablename__ = 'dogs'

    id = Column(Integer, primary_key=True)
    nickname = Column(String, nullable=False)
    breed = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False, default=0)
    FIO = Column(String, nullable=False)
    social_position = Column(Enum(SocialPosition), default=SocialPosition.student)
    date_of_birth = Column(DateTime, nullable=False)
    address = Column(String, nullable=False)

    dog_training_club_id = Column(Integer, ForeignKey('dogs_training_club.id'))
    dog_training_club = relationship("DogTrainingClub", back_populates="dogs")

    competitions = relationship("Competition", secondary=DogCompetitions.__table__, back_populates="dogs", lazy='joined')


class Competition(Base):
    __tablename__ = 'competitions'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    contribution = Column(Integer, nullable=False)
    viewers_quantity = Column(Integer, nullable=False)

    club_id = Column(Integer, ForeignKey('dogs_training_club.id'), nullable=False)
    club = relationship("DogTrainingClub", back_populates="competitions")
    dogs = relationship("Dog", secondary=DogCompetitions.__table__, lazy='joined')


class Permission(BasePermission, Base):
    __tablename__ = 'permissions'


class UserSession(BaseUserSession, Base):
    __tablename__ = 'user_sessions'


DBSession = database.create_session("DBSession")
BlockSession = database.create_session("BlockSession")
