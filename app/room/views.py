import json

from flask import jsonify, request

from app import db, socketio
from app.models.room import Room, RoomAssociation
from app.models.collection import Collection
from app.models.schemas import (room_share_schema, user_share_schema,
                                users_share_schema, collection_share_schema)
from app.wrappers import token_required

from . import room


@room.route('/', methods=['POST'])
@token_required
def create_room(user):
    body = request.get_json()

    if body['code'] and body['collection_id']:
        collection = Collection.query.filter_by(
            id=body['collection_id']).first()

        if collection is None:
            return jsonify({'message': 'Collection not found'}), 404

        existing_active_room = Room.query.filter_by(
            code=body['code'], status='active').first()

        existing_waiting_room = Room.query.filter_by(
            code=body['code'], status='waiting').first()

        if existing_active_room is not None or existing_waiting_room is not None:
            res = {
                'message': f"Room '{body['code']}' is already in use"
            }

            return jsonify(res), 403

        existing_association = RoomAssociation.query.filter_by(
            user_id=user.id).first()

        # If user belongs to a room, remove him from there
        if existing_association is not None:
            Room.query.filter_by(
                id=existing_association.room_id).first().remove_user(user.id)

        new_room = Room.query.filter_by(
            code=body['code'], status='inactive').first()

        if new_room is None:
            new_room = Room(code=body['code'],
                            created_by=user.id, status='waiting', collection_id=body['collection_id'])

            db.session.add(new_room)
            db.session.commit()

        else:
            new_room.created_by = user.id
            new_room.status = 'waiting'

        new_join = RoomAssociation(user_id=user.id, room_id=new_room.id)

        db.session.add(new_join)
        db.session.commit()

        room_data = room_share_schema.dump(new_room)
        room_data['collection'] = collection_share_schema.dump(
            new_room.collection)
        room_data['users'] = users_share_schema.dump(new_room.users)
        room_data['game'] = None

        res = {
            'data': room_data
        }

        return jsonify(res)

    else:
        return jsonify({'message': 'Missing data in body'}), 422


@room.route('/', methods=['GET'])
@token_required
def get_current_room(user):
    association = RoomAssociation.query.filter_by(user_id=user.id).first()

    if association is None:
        return jsonify({'rooms': None}), 200

    else:
        room = Room.query.filter_by(id=association.room_id).first()

        res = {
            'room': room_share_schema.dump(room),
        }

        return jsonify(res)


@room.route('/<room_code>', methods=['GET'])
@token_required
def get_room_info(user, room_code):
    room = Room.query.filter_by(code=room_code).first()

    if room is None:
        return jsonify({'message': 'Room not found'}), 404

    else:
        res = {
            'data': room_share_schema.dump(room)
        }

        return jsonify(res)


@room.route('/<room_code>', methods=['POST'])
@token_required
def join_room(user, room_code):
    room = Room.query.filter_by(code=room_code).first()

    if room is None or room.status == 'inactive':
        return jsonify({'message': 'Room not found'}), 404

    if room.status == 'active':
        return jsonify({'message': 'Room is currently hosting a game'}), 422

    else:
        if len(room.users) == 8:
            return jsonify({'message': 'Room is full'}), 422

        existing_association = RoomAssociation.query.filter_by(
            user_id=user.id).first()

        # If user belongs to a room, remove him from there
        if existing_association is not None:
            Room.query.filter_by(
                id=existing_association.room_id).first().remove_user(user.id)

        room.add_user(user.id)

        room_data = room_share_schema.dump(room)
        room_data['collection'] = collection_share_schema.dump(room.collection)
        room_data['users'] = users_share_schema.dump(room.users)
        room_data['game'] = room.load_game()

        res = {
            'data': room_data
        }

        return jsonify(res), 200


@room.route('/<room_code>/game', methods=['GET'])
@token_required
def get_game_data(user, room_code):
    room = Room.query.filter_by(code=room_code).first()

    if room is None:
        return jsonify({'message': 'Room not found'}), 404

    else:
        game = room.load_game()

        if game is not None:
            res = {
                'data': game.load_game_data()
            }

            return jsonify(res)

        else:
            res = {
                'data': None
            }

            return jsonify(res)

# View may delete the room association and the room itself.
# REST calls should limit to only one databse change per request
@room.route('/<room_code>', methods=['DELETE'])
@token_required
def leave_room(user, room_code):
    room = Room.query.filter_by(code=room_code).first()

    if room is None:
        return jsonify({'message': 'Room not found'}), 404

    else:
        if user in room.users:
            room.remove_user(user.id)

            res = {
                'message': 'User removed',
                'room': room_share_schema.dump(room)
            }

            return jsonify(res), 200

        else:
            res = {
                'message': 'User is not in this room'
            }

            return jsonify(res), 422
