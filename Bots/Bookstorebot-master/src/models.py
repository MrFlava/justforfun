from botmanlib.models import DB, User as BUser, Permission as BPermission, users_permissions_table
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship

database = DB()
Base = database.Base


class User(BUser, Base):
    __tablename__ = 'users'
    permissions_association_table = users_permissions_table(Base.metadata)
    came_from = Column(String)
    has_order = Column(Boolean, default=False)

    def init_permissions(self):
        for permission in ['start_menu_access',
                           'profile_menu_access',
                           'change_language_menu_access',
                           'marketplace_menu_access',
                           'price_analysis_menu_access',
                           'make_query_menu_access',
                           'queries_history_menu_access',
                           'buy_queries_menu_access',
                           'operators_menu_access']:
            perm = DBSession.query(Permission).get(permission)
            if perm not in self.permissions:
                self.permissions.append(perm)


class Permission(BPermission, Base):
    __tablename__ = 'permissions'


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    genre = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    image = Column(String)
    price = Column(Integer)

DBSession = database.DBSession
Base.metadata.create_all(database.engine)
