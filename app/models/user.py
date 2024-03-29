from app import db
from app.models.collection import Collection, OwnedCollection
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from flask import current_app


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    fb_id = db.Column(db.String)
    name = db.Column(db.String)
    username = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    profile_img = db.Column(db.String)
    profile_color = db.Column(db.String)
    source = db.Column(db.String)
    collections = db.relationship('Collection', secondary='owned_collections')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def create_default_collection(self):
        default_collection = Collection(
            name='Minhas cartas', created_by=self.id, editable=False)

        db.session.add(default_collection)
        db.session.commit()

        ownership = OwnedCollection(
            collection_id=default_collection.id, user_id=self.id)

        db.session.add(ownership)
        db.session.commit()

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration):
        token = jwt.encode({'id': self.id, 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(seconds=expiration)}, current_app.config['SECRET_KEY'])

        return token

    @staticmethod
    def verify_auth_token(token):
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'])

        except:
            return None

        return User.query.get(data['id'])
