from app import db
from datetime import datetime

class Association(db.Model):
    __tablename__ = 'association'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), primary_key=True)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow())

class Room(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(5))
    users = db.relationship("User", secondary='association')