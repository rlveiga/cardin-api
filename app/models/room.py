import json
from datetime import datetime
from enum import Enum

from flask import jsonify

from app import db
from app.models.schemas import (card_share_schema, room_share_schema,
                                user_share_schema, users_share_schema)

class RoomAssociation(db.Model):
    __tablename__ = 'room_association'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)

class Room(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(12), nullable=False)
    status = db.Column(db.String(64), default='active', nullable=False)
    created_by = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    data = db.Column(db.String(1024))
    users = db.relationship("User", secondary='room_association')

    def init_game(self, collection):
        self.reset_game()
        self.create_deck(collection)
        
        db.session.commit()

    # Game state is stored as data
    def reset_game(self):
        data = {
            'state': 'Zero',
            'deck': [],
            'hands': [[]] * 4,
            'scores': [0] * 4,
        }

        self.data = json.dumps(data)

    def load_game(self):
        return json.loads(self.data)

    def update_game(self, data):
        pass

    def create_deck(self, collection):
        game = self.load_game()

        for card in collection:
            game['deck'].append(card_share_schema.dump(card))

        self.data = json.dumps(game)

    #shuffles and distributes cards
    def shuffle_deck(self, user_id):
        pass
