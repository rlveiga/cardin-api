import json
import random
from datetime import datetime
from enum import Enum

from flask import jsonify

from app import db
from app.models.schemas import (card_share_schema, cards_share_schema,
                                collection_share_schema, room_share_schema,
                                user_share_schema, users_share_schema)
from app.models.user import User
from app.models.game import Game


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
    status = db.Column(db.String(64), default='waiting', nullable=False)
    created_by = db.Column(db.Integer)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow(), nullable=False)
    discarded_at = db.Column(db.DateTime)
    games = db.relationship("Game", backref='room')
    # game_data = db.Column(db.String(500000))
    users = db.relationship("User", secondary='room_association')

    def create_new_game(self):
        game = Game(room_id=self.id)

        db.session.add(game)
        db.session.commit()

    def start_new_game(self, collection):
        game = self.load_game()

        if game is not None:
            game.start_game(collection)

    def add_user(self, user_id):
        new_join = RoomAssociation(user_id=user_id, room_id=self.id)

        db.session.add(new_join)
        db.session.commit()

        active_game = self.load_game()

        if active_game is not None:
            game_data = active_game.load_game_data()

            user_dict = user_share_schema.dump(
                User.query.filter_by(id=user_id).first())

            game_data['players'].append({
                'data': user_dict,
                'hand': [],
                'score': 0,
                'is_ready': False
            })

            self.game_data = json.dumps(game_data)

    def remove_user(self, user_id):
        association = RoomAssociation.query.filter_by(
            room_id=self.id, user_id=user_id).first()

        db.session.delete(association)

        db.session.commit()

        active_game = self.load_game()

        if active_game is not None:
            game_data = active_game.load_game_data()

            for player in game_data['players']:
                if player['data']['id'] == user_id:
                    game_data['players'].remove(player)

            if len(game_data['players']) < 3 and self.status == 'active':
                self.status = 'inactive'

            self.game_data = json.dumps(game_data)

    def load_game(self):
        last_game = Game.query.filter_by(
            room_id=self.id, discarded_at=None).first()

        return last_game
