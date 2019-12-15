from flask import jsonify, Blueprint, current_app, request, make_response
from app import db
from app.models.user import User
from app.models.schemas import user_share_schema, users_share_schema
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