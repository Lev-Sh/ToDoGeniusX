import sqlalchemy as sa
from sqlalchemy import orm

from .users import User
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin

class Card(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'cards'

    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey(User.id), default=1)
    name = sa.Column(sa.String)
    top_px = sa.Column(sa.Integer, default=100)
    left_px = sa.Column(sa.Integer, default=100)
    color = sa.Column(sa.String, default='(245, 222, 179)')

    user = orm.relationship('User')
