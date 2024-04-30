import json
import flask
from flask import jsonify, request, make_response
import re
from data.db_models import db_session
from data.db_models.cards import Card

blueprint = flask.Blueprint(
    'cards_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/cards/<int:card_id>/<int:left_px>/<int:top_px>', methods=['PUT'])
def move_card(card_id, left_px, top_px):
    db_sess = db_session.create_session()
    card = db_sess.query(Card).get(card_id)
    card.left_px = left_px
    card.top_px = top_px
    db_sess.commit()
    return 'ok'


@blueprint.route('/api/cards/<int:card_id>', methods=['DELETE'])
def name_of_card(card_id):
    db_sess = db_session.create_session()
    card = db_sess.query(Card).get(card_id)
    db_sess.delete(card)
    db_sess.commit()
    return 'ok'


@blueprint.route('/api/cards/<int:user_id>', methods=['GET'])
def get_cards(user_id):
    db_sess = db_session.create_session()
    cards = db_sess.query(Card).filter(Card.user_id.like(user_id)).all()
    all_cards = []
    for i in cards:
        all_cards.append({f'Card':
                              i.to_dict(only=('id','name', 'top_px', 'left_px', 'user.name', 'content'))})
    return jsonify(all_cards)


@blueprint.route('/api/cards', methods=['POST'])
def create_cards():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['name', 'top_px', 'left_px', 'color', 'user_id']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    card = Card(
        name=request.json['name'],
        top_px=request.json['top_px'],
        left_px=request.json['left_px'],
        color=request.json['color'],
        user_id=request.json['user_id']
    )
    db_sess.add(card)
    db_sess.commit()
    return str(card.id)
