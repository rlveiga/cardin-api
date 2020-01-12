from flask import jsonify, Blueprint, current_app, request, make_response
from app import db
from app.models.user import User
from app.models.room import Room, Association
from app.models.card import Card
from app.models.collection import Collection
from app.models.schemas import cards_share_schema, collection_share_schema, user_share_schema, users_share_schema, room_share_schema
from . import main
from functools import wraps
import jwt

def token_required(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        token = request.headers.get('access-token')

        if not token:
            return jsonify({'message': 'Token required'}), 403

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            
            user = User.query.filter_by(id=data['id']).first()

        except:
            return jsonify({'message': 'Authentication failed'}), 403

        return fn(user, **kwargs)

    return decorated
        
@main.route('/users/', methods=['GET'])
@token_required
def index(user):
    res = {
        'user': user_share_schema.dump(user)
    }

    return jsonify(res)

@main.route('/auth/login', methods=['POST'])
def login():
    body = request.get_json()
    user = User.query.filter_by(username=body['username']).first()
    
    if(user is None):
        res = {
            'message': 'Não exisite um usuário com este username'
        }

        return make_response(res, 404)
        
    if(user.verify_password(body['password'])):
        token = user.generate_auth_token(3600).decode('UTF-8')
        
        res = {
            'user': user_share_schema.dump(user),
            'token': token
        }

        return jsonify(res)

    else:
        res = {
            'success': False,
            'message': 'Invalid credentials'
        }

        return make_response(res, 401)

@main.route('/rooms', methods=['POST'])
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

@main.route('/rooms', methods=['GET'])
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

@main.route('/rooms/<room_code>', methods=['GET'])
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
    
@main.route('/rooms/<room_code>', methods=['POST'])
@token_required
def join_room(user, room_code):
    room = Room.query.filter_by(code=room_code,status='active').first()

    if room is None:
        return jsonify({'message': 'Room not found'}), 404

    else:
        response = room.add_player(user.id)

        return jsonify(response)

@main.route('/rooms/<room_id>', methods=['DELETE'])
@token_required
def leave_room(user, room_id):
    room = Room.query.filter_by(id=room_id).first()

    if room is None:
        return jsonify({'message': 'Room not found'}), 404

    else:
        response = room.remove_player(user.id)

        return jsonify(response)

@main.route('/cards', methods=['GET'])
@token_required
def get_user_cards(user):
    cards = Card.query.filter_by(created_by=user.id).all()

    res = {
        'cards': cards_share_schema.dump(cards)
    }

    return jsonify(res)

@main.route('/collections', methods=['GET'])
@token_required
def get_user_collections(user):
    collections = Collection.query.filter_by(created_by=user.id).all()

    collection_list = []

    for col in collections:
        cards = Card.query.filter_by(collection_id=col.id).all()

        collection_list.append({
            'data': collection_share_schema.dump(col),
            'cards': cards_share_schema.dump(cards)
        })

    res = {
        'collections': collection_list
    }

    return jsonify(res)