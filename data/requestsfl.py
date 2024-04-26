from data.db_models import db_session
from data.db_models.cards import Card
from data.db_models.db_session import global_init

global_init('db/database.db')

db_sess = db_session.create_session()
cards = db_sess.query(Card).filter(Card.user_id == user_id).all()
print(cards)