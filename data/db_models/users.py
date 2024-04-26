import sqlalchemy as sa
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer,
                   primary_key=True, autoincrement=True)
    nickname = sa.Column(sa.String, nullable=True)
    name = sa.Column(sa.String, nullable=True)
    birthday = sa.Column(sa.Integer, nullable=True)
    email = sa.Column(sa.String, index=True, unique=True)
    hashed_password = sa.Column(sa.String)
    salt = sa.Column(sa.String)

    card = orm.relationship('Card', back_populates='user')
    notification = orm.relationship('Notification', back_populates='user')
