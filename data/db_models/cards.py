import sqlalchemy as sa
from sqlalchemy import orm

from .users import User
from .db_session import SqlAlchemyBase


class Card(SqlAlchemyBase):
    __tablename__ = 'cards'

    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey(User.id))
    name = sa.Column(sa.String)
    top_px = sa.Column(sa.REAL, default=100)
    left_px = sa.Column(sa.REAL, default=100)
    color = sa.Column(sa.String, default='(245, 222, 179)')

    user = orm.relationship('User')
