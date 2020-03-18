import json

from flask import jsonify, request

from app import db, socketio
from app.models.room import Room, RoomAssociation
from app.models.collection import Collection
from app.models.schemas import (room_share_schema, user_share_schema,
                                users_share_schema)
from app.wrappers import token_required

from . import room


@room.route('/', methods=['POST'])
@token_required
def create_room(user):
    existing_association = RoomAssociation.query.filter_by(
        user_id=user.id).first()

    if existing_association is not None:
        res = {
            'message': 'User already belongs to a room'
        }

        return jsonify(res), 403

    body = request.get_json()

    if(body['code']):
        existing_room = Room.query.filter_by(
            code=body['code'], status='active').first()

        if existing_room:
            res = {
                'message': f"Room '{body['code']}' is already in use"
            }

            return jsonify(res), 403

        new_room = Room(code=body['code'], created_by=user.id)

        db.session.add(new_room)
        db.session.commit()

        new_join = RoomAssociation(user_id=user.id, room_id=new_room.id)

        db.session.add(new_join)
        db.session.commit()

        collection = Collection.query.filter_by(
            id=body['collection_id']).first()

        if collection is None:
            res = {
                'message': 'Collection not found'
            }

            return res, 404

        new_room.init_room(collection)

        res = {
            'data': room_share_schema.dump(new_room),
            'game': new_room.load_game(),
            'users': users_share_schema.dump(new_room.users)
        }

        return jsonify(res)

    else:
        return jsonify({'message': 'Missing code in body'}), 422


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
    room = Room.query.filter_by(code=room_code, status='active').first()

    if room is None:
        return jsonify({'message': 'Room not found'}), 404

    else:
        players_list = []

        for member in room.users:
            players_list.append({
                'data': user_share_schema.dump(member),
                'score': 0
            })

        res = {
            'room': {
                'data': room_share_schema.dump(room),
                'users': players_list
            }
        }

        return jsonify(res)


@room.route('/<room_code>', methods=['POST'])
@token_required
def join_room(user, room_code):
    room = Room.query.filter_by(code=room_code, status='active').first()

    if room is None:
        return jsonify({'message': 'Room not found'}), 404

    else:
        existing_association = RoomAssociation.query.filter_by(
            user_id=user.id).first()

        if existing_association is not None:
            res = {
                'message': 'User already belongs to a room'
            }

            return jsonify(res), 403

        room.add_user(user)

        res = {
            'data': room_share_schema.dump(room),
            'users': users_share_schema.dump(room.users),
            'game': room.load_game()
        }

        return jsonify(res), 200

# View may delete the room association and the room itself.
# REST calls should limit to only one databse change per request
@room.route('/<room_code>', methods=['DELETE'])
@token_required
def leave_room(user, room_code):
    room = Room.query.filter_by(code=room_code, status='active').first()

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