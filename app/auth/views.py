from flask import jsonify, request

from app import db
from app.models.user import User
from app.models.collection import Collection, OwnedCollections
from app.models.schemas import collections_share_schema, user_share_schema

from . import auth

@auth.route('/register', methods=['POST'])
def register():
    body = request.get_json()

    existing_user = User.query.filter_by(username=body['username']).first()

    if existing_user is not None:
        res = {
            'message': 'Username is taken'
        }

        return jsonify(res), 409

    else:
        new_user = User(username=body['username'])
        new_user.password = body['password']

        db.session.add(new_user)
        db.session.commit()

        default_collection = Collection(name='Minhas cartas', created_by=new_user.id, is_deletable=False)

        db.session.add(default_collection)
        db.session.commit()

        ownership = OwnedCollections(collection_id=default_collection.id, user_id=new_user.id)

        db.session.add(ownership)
        db.session.commit()

        user_response = user_share_schema.dump(new_user)
        user_response['collections'] = collections_share_schema.dump(new_user.collections)

        res = {
            'message': 'User created',
            'user': user_response
        }
        
        return jsonify(res), 201

@auth.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    user = User.query.filter_by(username=body['username']).first()
    
    if(user is None):
        res = {
            'message': 'Não exisite um usuário com este username'
        }

        return jsonify(res), 404
        
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

        return jsonify(res), 401