from flask import jsonify, request

from app import db
from app.models.card import Card
from app.models.collection import Collection
from app.models.schemas import card_share_schema, cards_share_schema, collection_share_schema, collections_share_schema
from . import collection
from app.wrappers import token_required
from app.utils import user_owns_collection

@collection.route('/<collection_id>', methods=['GET'])
@token_required
def get_collection_info(user, collection_id):
  collection = Collection.query.filter_by(id=collection_id).first()

  if collection is None:
    res = {
      'message': 'Collection not found'
    }

    return jsonify(res), 404

  if user_owns_collection(user.id, collection.id) is False:
    res = {
      'message': 'You do not own this collection'
    }

    return jsonify(res), 403

  collection_obj = collection_share_schema.dump(collection)
  collection_obj['cards'] = cards_share_schema.dump(collection.cards)

  res = {
    'collection': collection_obj
  }

  return jsonify(res)

@collection.route('/', methods=['GET'])
@token_required
def get_user_collections(user):
  collections = user.collections

  data = []

  for e in collections:
    card_count = len(e.cards)
    e = collection_share_schema.dump(e)
    e['card_count'] = card_count

    data.append(e)

  res = {
      'collections': data
  }

  return jsonify(res)

@collection.route('/', methods=['POST'])
@token_required
def create_collection(user):
    body = request.get_json()

    new_collection = Collection(name=body['name'], created_by=user.id)

    db.session.add(new_collection)
    db.session.commit()

    res = {
        'collection': {
            'data': collection_share_schema.dump(new_collection),
            'cards': []
        }
    }

    return jsonify(res), 201

@collection.route('/<collection_id>', methods=['DELETE'])
@token_required
def delete_collection(user, collection_id):
    collection = Collection.query.filter_by(id=collection_id).first()

    # Repeating code here
    if collection is None:
        res = {
            'message': 'Collection not found'
        }

        return jsonify(res), 404

    else:
        # Repeating code again, should create a wrapper that
        # checks if user actually owns the collection
        if collection.created_by != user.id:
            res = {
                'message': 'You do not own this collection'
            }

            return jsonify(res), 401
            
        else:
            db.session.delete(collection)
            db.session.commit()

            res = {
                'message': 'Collection deleted',
                'collection': collection_share_schema.dump(Collection.query.filter_by(id=collection_id).first())
            }

            return jsonify(res), 200

@collection.route('/<collection_id>/cards', methods=['GET'])
@token_required
def get_cards_from_collection(user, collection_id):
    collection = Collection.query.filter_by(id=collection_id).first()

    if collection is None:
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
            res = {
                'cards': cards_share_schema.dump(collection.cards)
            }

            return jsonify(res)
