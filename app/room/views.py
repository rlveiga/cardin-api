import json

from flask import jsonify, request
from flask_socketio import emit, join_room, leave_room

from app import db, socketio
from app.models.room import Room, RoomAssociation
from app.models.schemas import (room_share_schema, user_share_schema,
                                users_share_schema)
from app.wrappers import token_required

from . import room

@socketio.on('join')
def on_join(data):
  print(data)
  room = data['room']
  user = data['user']

  join_room(room)
  emit('new_join', {"user": user, "room": room}, broadcast=True)

@socketio.on('leave')
def on_leave(data):
  print(data)
  room = data['room']
  user = data['user']

  leave_room(room)
  emit('new_leave', {"user": user, "room": room}, broadcast=True)

@room.route('/', methods=['POST'])
@token_required
def create_room(user):
    existing_association = RoomAssociation.query.filter_by(user_id=user.id).first()

    if existing_association is not None:
      res = {
        'message': 'User already belongs to a room'
      }

      return jsonify(res), 403

    body = request.get_json()

    if(body['code']):
        existing_room = Room.query.filter_by(code=body['code'], status='active').first()

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
      existing_association = RoomAssociation.query.filter_by(user_id=user.id).first()

      if existing_association is not None:
        res = {
            'message': 'User already belongs to a room'
        }

        return jsonify(res), 403

      if len(room.users) < 4:
          new_join = RoomAssociation(user_id=user.id, room_id=room.id)

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

@room.route('/<room_code>', methods=['DELETE'])
@token_required
def leave_room(user, room_code):
    room = Room.query.filter_by(code=room_code, status='active').first()

    if room is None:
        return jsonify({'message': 'Room not found'}), 404

    else:
        if user in room.users:
          # Host has left the room, make room inactive
          # and remove all players
          if room.created_by == user.id:
              for u in room.users:
                u_association = RoomAssociation.query.filter_by(room_id=room.id, user_id=u.id).first()

                db.session.delete(u_association)
                
              room.status = 'inactive'

          else:
            association = RoomAssociation.query.filter_by(room_id=room.id, user_id=user.id).first()

            db.session.delete(association)
          db.session.commit()
          
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

@room.route('/start_game', methods=['PUT'])
def start_game():
  room_code = request.args.get('room')

  room = Room.query.filter_by(code=room_code, status='active').first()

  if room is not None:
    room.init_game()

    res = {
      'users': users_share_schema.dump(room.users),
      'room': room_share_schema.dump(room)
    }

    res['room']['data'] = json.loads(room.data)

    return jsonify(res), 201
