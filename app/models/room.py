import json
import random

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

    def init_room(self, collection):
        self.reset_game_data(collection)
        self.create_deck(collection.cards)

        db.session.commit()

    # Game state is stored as metadata
    def reset_game_data(self, collection):
        collection_dict = collection_share_schema.dump(collection)
        collection_dict['card_count'] = len(collection.cards)

        game_data = {
            'state': 'Zero',
            'collection': collection_dict,
            'all_cards': [],
            'white_cards': [],
            'black_cards': [],
            'discarded_cards': [],
            'table_card': None,
            'hands': [{
                'user_id': self.created_by,
                'cards': []
            }],
            'selected_cards': [{
                'user_id': self.created_by,
                'cards': None
            }],
            'scores': [{
                'user_id': self.created_by,
                'score': 0
            }],
            'czar_id': None
        }

        self.game_data = json.dumps(game_data)

    def create_deck(self, cards):
        game_data = self.load_game()
        game_data['all_cards'] = cards_share_schema.dump(cards)

        for card in cards:
            if(card.card_type == 'black'):
                game_data['black_cards'].append(card_share_schema.dump(card))

            elif(card.card_type == 'white'):
                game_data['white_cards'].append(card_share_schema.dump(card))

        self.game_data = json.dumps(game_data)

    def init_game(self):
        self.distribute_cards()
        self.pick_table_card()
        self.pick_czar()

    # Randomly assigns white cards to hands,
    # to be called upon game start
    def distribute_cards(self):
        game_data = self.load_game()
        white_card_list = game_data['white_cards']

        for hand in game_data['hands']:
            for i in range(7):
                selected_card = white_card_list.pop(
                    random.randrange(len(white_card_list)))

                hand['cards'].append(selected_card)
                game_data['discarded_cards'].append(selected_card)

        self.game_data = json.dumps(game_data)

    # Randomly select a card prom black cards to
    # be played, to be called upon game start and
    # round end
    def pick_table_card(self):
        game_data = self.load_game()
        black_card_list = game_data['black_cards']

        selected_card = black_card_list.pop(
            random.randrange(len(black_card_list)))
        game_data['table_card'] = selected_card
        game_data['discarded_cards'].append(selected_card)

        self.game_data = json.dumps(game_data)

    def pick_czar(self):
        game_data = self.load_game()
        new_czar_id = self.users[random.randrange(len(self.users))].id

        game_data['czar_id'] = new_czar_id
        self.game_data = json.dumps(game_data)

    def add_user(self, user_id):
        new_join = RoomAssociation(user_id=user_id, room_id=self.id)

        db.session.add(new_join)
        db.session.commit()

        game_data = self.load_game()
        game_data['hands'].append({
            'user_id': user_id,
            'cards': []
        })
        game_data['selected_cards'].append({
            'user_id': user_id,
            'cards': []
        })
        game_data['scores'].append({
            'user_id': user_id,
            'score': 0
        })

        self.game_data = json.dumps(game_data)

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

    def set_cards_for_user(self, user_id, user_cards):
        game_data = self.load_game()

        for data in game_data['selected_cards']:
            if data['user_id'] == user_id:
                data['cards'] = user_cards

        for hand in game_data['hands']:
            if hand['user_id'] == user_id:
                print(f"Hand: {hand['cards']}")
                for selected_card in user_cards:
                    hand['cards'].remove(selected_card)
                    
        self.game_data = json.dumps(game_data)

    def load_game(self):
        game_data = json.loads(self.game_data)

        return game_data
