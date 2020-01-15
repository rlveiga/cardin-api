from flask import jsonify, request, current_app

from app.models.user import User

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