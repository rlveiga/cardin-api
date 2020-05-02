from flask import jsonify, request

from app import db
from app.models.user import User
from app.models.collection import Collection, OwnedCollection
from app.models.schemas import collections_share_schema, user_share_schema

from . import auth

import requests


@auth.route('/', methods=['POST'])
def authenticate():
    body = request.get_json()
    fb_access_token = body['fb_access_token']

    if fb_access_token is None:
        return jsonify({'message': 'User must provide Facebook access token'}), 422

    fb_res = requests.get(
        f"https://graph.facebook.com/debug_token?input_token={fb_access_token}&access_token=731854590887475|pFECnCSWTIvaybrkcqOUauK65Ws").json()

    data = fb_res.get('data') 

    if data.get('error') is not None:
        return jsonify({'message': 'Failed to authenticate'}), 403

    fb_id = data['user_id']

    user = User.query.filter_by(fb_id=fb_id).first()
    
    if user is None:
        user_info = requests.get(
            f"https://graph.facebook.com/{fb_id}?fields=id,name,picture.width(200).height(200)&access_token={fb_access_token}").json()

        user = User(name=user_info['name'],
                    profile_img=user_info['picture']['data']['url'],
                    fb_id=fb_id,
                    source='fb')

        db.session.add(user)
        db.session.commit()

        user.create_default_collection()

    token = user.generate_auth_token(3600).decode('UTF-8')

    res = {
        'user': user_share_schema.dump(user),
        'token': token
    }

    return jsonify(res)


# Registration of user without Facebook account
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
        new_user = User(username=body['username'], source='cardin')
        new_user.password = body['password']

        db.session.add(new_user)
        db.session.commit()

        new_user.create_default_collection()

        user_response = user_share_schema.dump(new_user)

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
