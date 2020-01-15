from flask import jsonify, request

from app import db
from app.models.room import Room, Association
from app.models.schemas import room_share_schema, user_share_schema, users_share_schema
from . import room
from app.wrappers import token_required

@room.route('/', methods=['POST'])
@token_required
def create_room(user):
    body = request.get_json()

    if(body['code']):
        new_room = Room(code=body['code'], created_by=user.id)

        db.session.add(new_room)
        db.session.commit()

        new_join = Association(user_id=user.id, room_id=new_room.id)

        db.session.add(new_join)
        db.session.commit()

        room = {
            'data': room_share_schema.dump(new_room),
            'users': users_share_schema.dump(new_room.users)
        }

        res = {
            'room': room
        }

        return jsonify(res)

    else:
        return jsonify({'message': 'Missing code in body'}), 422

@room.route('/', methods=['GET'])
@token_required
def get_current_room(user):
    association = Association.query.filter_by(user_id=user.id).first()

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
            'sucess': True,
            'room': {
                'data': room_share_schema.dump(room),
                'users': players_list
            }
        }
        
        return jsonify(res)
    
@room.route('/<room_code>', methods=['POST'])
@token_required
def join_room(user, room_code):
    room = Room.query.filter_by(code=room_code,status='active').first()

    if room is None:
        return jsonify({'message': 'Room not found'}), 404

    else:
        if len(room.users) < 4:
            if user in room.users:
                res = {
                    'message': 'User is already in this room'
                }

                return jsonify(res), 422
            
            else:
                new_join = Association(user_id=user.id, room_id=room.id)

                db.session.add(new_join)
                db.session.commit()

                res = {
                    'room': {
                        'data': room_share_schema.dump(room),
                        'users': users_share_schema.dump(room.users)
                    }
                }

                return jsonify(res), 200

        else:
            res = {
                'message': 'Room is full'
            }

            return jsonify(res), 422

@room.route('/<room_id>', methods=['DELETE'])
@token_required
def leave_room(user, room_id):
    room = Room.query.filter_by(id=room_id).first()

    if room is None:
        return jsonify({'message': 'Room not found'}), 404

    else:
        if user in room.users:
            association = Association.query.filter_by(room_id=room.id, user_id=user.id).first()

            db.session.delete(association)
            db.session.commit()
            
            res = {
                'message': 'User removed'
            }

            return jsonify(res), 200

        else:
            res = {
                'message': 'User is not in this room'
            }

            return jsonify(res), 422