from app import db
from app.models.schemas import user_share_schema, users_share_schema, room_share_schema, card_share_schema
from datetime import datetime
from enum import Enum
from flask import jsonify

import json

class Association(db.Model):
    __tablename__ = 'association'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    date_joined = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)

class Room(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(64), default='active')
    created_by = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    code = db.Column(db.String(12))
    state = db.Column(db.String(1024))
    users = db.relationship("User", secondary='association')

    def init_game(self, cards):
        self.reset_state()
        self.create_deck(cards)
        
        db.session.commit()

    def reset_state(self):
        state = {
            'game_state': 'Zero',
            'deck': [],
            'hands': [[]] * 4,
            'turn': 0,
            'scores': [0] * 4,
        }

        self.state = json.dumps(state)

    def load_state(self):
        return json.loads(self.state)

    def create_deck(self, collection):
        state = self.load_state()

        for card in collection:
            state['deck'].append(card_share_schema.dump(card))

        self.state = json.dumps(state)

    #shuffles and distributes cards
    def shuffle_deck(self, user_id):
        pass        

    def add_player(self, user_id):
        if len(self.users) < 4:
            new_join = Association(user_id=user_id, room_id=self.id)

            db.session.add(new_join)
            db.session.commit()

            return {
                'success': True,
                'room': {
                    'data': room_share_schema.dump(self),
                    'users': users_share_schema.dump(self.users)
                }
            }

        else:
            return {
                'success': False,
                'message': 'Room is full'
            }
    
    def remove_player(self, user_id):
        for u in self.users:
            if u.id == user_id:
                association = Association.query.filter_by(room_id=self.id, user_id=user_id).first()

                db.session.delete(association)
                db.session.commit()
                
                return {
                    'success': True,
                    'message': 'User removed'
                }

        else:
            return {
                'success': False,
                'message': 'User is not in this room'
            }