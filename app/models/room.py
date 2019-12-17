from app import db
from datetime import datetime

class Association(db.Model):
    __tablename__ = 'association'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)

class Room(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(5))
    users = db.relationship("User", secondary='association')