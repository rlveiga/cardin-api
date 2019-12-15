from app import db
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from flask import current_app

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def generate_auth_token(self, expiration):
        token = jwt.encode({'id': self.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expiration)}, current_app.config['SECRET_KEY'])
        
        return token
        
    @staticmethod
    def verify_auth_token(token):
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'])

        except:
             return None
             
        return User.query.get(data['id'])