from flask import jsonify, request

from app import db
from app.models.card import Card
from app.models.collection import Collection
from app.models.schemas import card_share_schema, cards_share_schema, collection_share_schema, user_share_schema, users_share_schema, room_share_schema

from . import card
from app.wrappers import token_required
from functools import wraps

@card.route('/', methods=['POST'])
@token_required
def create_card(user):
    body = request.get_json()

    if(body['name'] and body['card_type']):
        new_card = Card(name=body['name'], card_type=body['card_type'], created_by=user.id)

        db.session.add(new_card)
        db.session.commit()

        res = {
            'message': 'Card created',
            'card': card_share_schema.dump(new_card)
        }

        return jsonify(res)

    else:
        res = {
            'message': 'Missing attributes'
        }

        return jsonify(res), 422

@card.route('/', methods=['GET'])
@token_required
def get_user_cards(user):
    cards = Card.query.filter_by(created_by=user.id).all()

    res = {
        'cards': cards_share_schema.dump(cards)
    }

    return jsonify(res)

@card.route('/<card_id>', methods=['DELETE'])
@token_required
def delete_card(user, card_id):
    card = Card.query.filter_by(id=card_id).first()

    if card is None:
        res = {
            'message': 'Card not found'
        }

        return jsonify(res), 404

    else:
        if card.created_by != user.id:
            res = {
                'message': 'You do not own this card'
            }

            return jsonify(res), 401

        else:
            db.session.delete(card)
            db.session.commit()

            res = {
                'message': 'Card deleted',
                'card': card_share_schema.dump(Card.query.filter_by(id=card_id).first())
            }

            return jsonify(res)

@card.route('/<card_id>/add_collection/<collection_id>', methods=['PUT'])
@token_required
def add_card_to_collection(user, card_id, collection_id):
    card = Card.query.filter_by(id=card_id).first()
    collection = Collection.query.filter_by(id=collection_id).first()

    if card is None:
        print('a')
        res = {
            'message': 'Card not found'
        }

        return jsonify(res), 404

    elif collection is None:
        res = {
            'message': 'Collection not found'
        }

        return jsonify(res), 404

    else:
        if collection.created_by != user.id:
            res = {
                'message': 'You do not own this collection'
            }

            return jsonify(res), 401

        else:
            card.collection_id = collection.id

            db.session.add(card)
            db.session.commit()

            res = {
                'message': 'Card added to collection',
                'card': card_share_schema.dump(card)
            }

            return jsonify(res)