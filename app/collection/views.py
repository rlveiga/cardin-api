from flask import jsonify, request

from app import db
from app.models.card import Card, CardAssociation
from app.models.collection import Collection, OwnedCollection
from app.models.schemas import card_share_schema, cards_share_schema, collection_share_schema, collections_share_schema
from . import collection, owned_collection
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
    e = collection_share_schema.dump(e)

    data.append(e)

  res = {
      'collections': data
  }

  return jsonify(res)

@owned_collection.route('/<collection_id>', methods=['POST'])
@token_required
def create_owned_collection(user, collection_id):
  if user_owns_collection(user.id, collection_id) is True:
    return jsonify({'message': 'You already own this collection'}), 422

  collection = Collection.query.filter_by(id=collection_id).first()

  if collection is None:
    return jsonify({'message': 'Collection not found'}), 404

  owned_collection = OwnedCollection(user_id=user.id, collection_id=collection_id)

  db.session.add(owned_collection)
  db.session.commit()

  res = {
    'data': collection_share_schema.dump(collection)
  }

  return jsonify(res), 201

@owned_collection.route('/<collection_id>', methods=['DELETE'])
@token_required
def delete_owned_collection(user, collection_id):
  collection = Collection.query.filter_by(id=collection_id).first()

  if collection is None:
    return jsonify({'message': 'Collection not found'}), 404

  owned_collection = OwnedCollection.query.filter_by(user_id=user.id, collection_id=collection_id).first()

  if owned_collection is None:
    return jsonify({'message': 'You do not own this collection'}), 422

  db.session.delete(owned_collection)
  db.session.commit()

  return jsonify({
    'data': None
  })

@collection.route('/', methods=['POST'])
@token_required
def create_collection(user):
    body = request.get_json()

    new_collection = Collection(name=body['name'], created_by=user.id)
    db.session.add(new_collection)
    db.session.commit()

    new_collection.set_owner(user.id)

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

@collection.route('/<collection_id>/add_card/<card_id>', methods=['POST'])
@token_required
def add_card_to_collection(user, card_id, collection_id):
    card = Card.query.filter_by(id=card_id).first()
    collection = Collection.query.filter_by(id=collection_id).first()
    existing_association = CardAssociation.query.filter_by(card_id=card_id, collection_id=collection_id).first()

    if card is None:
        res = {
            'message': 'Card not found'
        }

        return jsonify(res), 404

    elif collection is None:
        res = {
            'message': 'Collection not found'
        }

        return jsonify(res), 404

    elif existing_association is not None:
        res = {
            'message': 'Card already belongs to this collection'
        }

        return jsonify(res), 409

    else:
        if collection.created_by != user.id:
            res = {
                'message': 'You do not own this collection'
            }

            return jsonify(res), 403

        else:
            existing_association
            new_association = CardAssociation(card_id=card.id, collection_id=collection.id)

            db.session.add(new_association)
            db.session.commit()

            collection_response = collection_share_schema.dump(collection)
            collection_response['cards'] = cards_share_schema.dump(collection.cards)

            res = {
                'message': 'Card added to collection',
                'collection': collection_response
            }

            return jsonify(res)

@collection.route('/<collection_id>/remove_card/<card_id>', methods=['DELETE'])
@token_required
def remove_card_from_collection(user, card_id, collection_id):
    card = Card.query.filter_by(id=card_id).first()
    collection = Collection.query.filter_by(id=collection_id).first()

    if card is None:
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
        if card.created_by != user.id:
            res = {
                'message': 'You do not own this card'
            }

            return jsonify(res), 403

        elif collection.created_by != user.id:
            res = {
                'message': 'You do not own this collection'
            }

            return jsonify(res), 403

        else:
            removed_association = CardAssociation.query.filter_by(card_id=card.id, collection_id=collection_id).first()

            if removed_association is None:
                res = {
                    'message': 'Card does not belong to this collection'
                }

                return jsonify(res), 404

            else:
                db.session.delete(removed_association)
                db.session.commit()

                res = {
                    'message': 'Card removed from collection'
                }

                return jsonify(res)