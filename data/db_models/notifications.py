import sqlalchemy as sa
from sqlalchemy import orm

from .users import User
from .db_session import SqlAlchemyBase


class Notification(SqlAlchemyBase):
    __tablename__ = 'notifications'

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey(User.id))
    notification_text = sa.Column(sa.String)
    creation_date = sa.Column(sa.DateTime)
    seen = sa.Column(sa.Integer, default=0)

    user = orm.relationship('User')
