import datetime

import sqlalchemy as sa
from .db_session import SqlAlchemyBase
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer,
                   primary_key=True, autoincrement=True)
    nickname = sa.Column(sa.String, nullable=True)
    name = sa.Column(sa.String, nullable=True)
    birthday = sa.Column(sa.Integer, nullable=True)
    email = sa.Column(sa.String, index=True, unique=True)
    hashed_password = sa.Column(sa.String)
    salt = sa.Column(sa.String)
