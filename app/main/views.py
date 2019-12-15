from flask import jsonify, Blueprint, request, make_response
from app import db
from app.models import User
from . import main

@main.route('/users/', methods=['GET'])
def index():
    users = User.query.all()
    user_list = []

    for u in users:
        user_list.append(u.serialize())

    res = {
        'users': user_list
    }

    return jsonify(res)

@main.route('/auth/login/', methods=['POST'])
def login():
    body = request.get_json()
    user = User.query.filter_by(email=body['email']).first()

    if(user is None):
        res = {
            'success': False
        }

        return make_response(res, 404)
    if(user.verify_password(body['password'])):
        token = user.generate_auth_token(3600).decode('UTF-8')
        
        res = {
            'user': user.serialize(),
            'token': token,
            'success': True
        }

        return jsonify(res)

    else:
        res = {
            'success': False
        }

        return jsonify(res)