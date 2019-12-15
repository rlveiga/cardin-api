from flask import jsonify, Blueprint, current_app, request, make_response
from app import db
from app.models.user import User
from app.models.room import Room, Association
from app.models.schemas import user_share_schema, users_share_schema, room_share_schema
from . import main
from functools import wraps
import jwt

def token_required(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        token = request.headers.get('access-token')

        if not token:
            return jsonify({'success': False, 'message': 'Token required'}), 403

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            
            user = User.query.filter_by(id=data['id']).first()

        except:
            return jsonify({'success': False, 'message': 'Authentication failed'}), 403

        return fn(user, **kwargs)

    return decorated
        
@main.route('/users/', methods=['GET'])
@token_required
def index(user):
    res = {
        'success': True,
        'user': user_share_schema.dump(user)
    }

    return jsonify(res)

@main.route('/auth/login', methods=['POST'])
def login():
    body = request.get_json()
    user = User.query.filter_by(email=body['email']).first()
    
    if(user is None):
        res = {
            'success': False,
            'message': 'Não exisite um usuário com este email'
        }

        return make_response(res, 404)
        
    if(user.verify_password(body['password'])):
        token = user.generate_auth_token(3600).decode('UTF-8')
        
        res = {
            'user': user_share_schema.dump(user),
            'token': token,
            'success': True
        }

        return jsonify(res)

    else:
        res = {
            'success': False,
            'message': 'Invalid credentials'
        }

        return jsonify(res)

@main.route('/rooms', methods=['POST'])
@token_required
def create_room(user):
    body = request.get_json()

    if(body['code']):
        new_room = Room(code=body['code'])

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
            'success': True,
            'room': room
        }

        return jsonify(res)

    else:
        return jsonify({'success': False, 'message': 'Missing code in body'}), 422

@main.route('/rooms/<room_id>', methods=['GET'])
@token_required
def get_room_info(user, room_id):
    room = Room.query.filter_by(id=room_id).first()

    if room is None:
        return jsonify({'success': False, 'message': 'Room not found'}), 404

    else:
        res = {
            'room': room_share_schema.dump(room),
            'users': users_share_schema.dump(room.users)
        }
        
        return jsonify(res)
    
@main.route('/rooms/<room_id>', methods=['POST'])
@token_required
def join_room(user, room_id):
    room = Room.query.filter_by(id=room_id).first()

    if room is None:
        return jsonify({'success': False, 'message': 'Room not found'}), 404

    else:
        join = Association(user_id=user.id, room_id=room_id)

        db.session.add(join)
        db.session.commit()

        room_obj = {
            'data': room_share_schema.dump(room),
            'users': users_share_schema.dump(room.users)
        }

        res = {
            'room': room_obj,
            'success': True
        }

        return jsonify(res)
