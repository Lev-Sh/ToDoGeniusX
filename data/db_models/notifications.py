import sqlalchemy as sa
from sqlalchemy import orm

from .users import User
from .db_session import SqlAlchemyBase


class Notification(SqlAlchemyBase):
    __tablename__ = 'notifications'

    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey(User.id))
    notification_id = sa.Column(sa.Integer)
    sample_id = sa.Column(sa.Integer)

    user = orm.relationship('User')
