from flask import jsonify, request

from app.models.user import User
from app.models.schemas import user_share_schema

from . import auth

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