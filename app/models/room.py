import json
from datetime import datetime
from enum import Enum

from flask import jsonify

from app import db
from app.models.schemas import (card_share_schema, cards_share_schema, room_share_schema,
                                collection_share_schema, user_share_schema, users_share_schema)


class RoomAssociation(db.Model):
    __tablename__ = 'room_association'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow(), nullable=False)


class Room(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(12), nullable=False)
    status = db.Column(db.String(64), default='active', nullable=False)
    created_by = db.Column(db.Integer)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow(), nullable=False)
    game_data = db.Column(db.String(500000))
    users = db.relationship("User", secondary='room_association')

    def init_game(self, collection):
        self.reset_game(collection)
        self.create_deck(collection.cards)

        db.session.commit()

    # Game state is stored as metadata
    def reset_game(self, collection):
        collection_dict = collection_share_schema.dump(collection)
        collection_dict['card_count'] = len(collection.cards)

        game_data = {
            'state': 'Zero',
            'collection': collection_dict,
            'all_cards': [],
            'white_cards': [],
            'black_cards': [],
            'hands': [[]],
            'scores': [{
                'user_id': self.created_by,
                'score': 0
            }],
        }

        self.game_data = json.dumps(game_data)

    def create_deck(self, cards):
        game_data = json.loads(self.game_data)
        game_data['all_cards'] = cards_share_schema.dump(cards)

        for card in cards:
            if(card.card_type == 'black'):
                game_data['black_cards'].append(card_share_schema.dump(card))

            elif(card.card_type == 'white'):
                game_data['white_cards'].append(card_share_schema.dump(card))

        self.game_data = json.dumps(game_data)

    def add_user(self, user_id):
        new_join = RoomAssociation(user_id=user_id, room_id=self.id)

        db.session.add(new_join)
        db.session.commit()

        game_data = self.load_game()
        game_data['hands'].append([])
        game_data['scores'].append({
            'user_id': user_id,
            'score': 0
        })

        self.game_data = json.dumps(game_data)
        db.session.commit()

    def remove_user(self, user_id):
        # Host has left the room, make room inactive
        # and remove all players
        if self.created_by == user_id:
            for u in self.users:
                u_association = RoomAssociation.query.filter_by(
                    room_id=self.id, user_id=u.id).first()

                db.session.delete(u_association)

            self.status = 'inactive'

        else:
            association = RoomAssociation.query.filter_by(
                room_id=self.id, user_id=user_id).first()

            db.session.delete(association)

        db.session.commit()

        game_data = self.load_game()

        for score in game_data['scores']:
            if score['user_id'] == user_id:
                game_data['scores'].remove(score)

        self.game_data = json.dumps(game_data)
        db.session.commit()

    def load_game(self):
        game_data = json.loads(self.game_data)

        print(game_data['scores'])

        return game_data
