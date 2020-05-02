from app import db
from app.models.card import Card, CardAssociation
from datetime import datetime


import csv


class OwnedCollection(db.Model):
    __tablename__ = 'owned_collections'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    collection_id = db.Column(db.Integer, db.ForeignKey('collections.id'))
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow(), nullable=False)


class Collection(db.Model):
    __tablename__ = 'collections'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    rooms = db.relationship("Room", backref='collection')
    cards = db.relationship('Card', secondary='card_association')
    owners = db.relationship('User', secondary='owned_collections')
    editable = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    created_by = db.Column(db.Integer)

    def create_from_file(self, folder_path, file_type):
        white_cards_path = f"./{folder_path}/white_cards.{file_type}"
        black_cards_path = f"./{folder_path}/black_cards.{file_type}"

        with open(white_cards_path) as card_file:
            if file_type == 'csv':
                csv_file = csv.reader(card_file, delimiter=';')

                for line in csv_file:
                    card_name = line[1]
                    self.create_card(card_name, 'white')

            else:
                for line in card_file:
                    card_name = line[:-1]

                    self.create_card(card_name, 'white')

        with open(black_cards_path) as card_file:
            if file_type == 'csv':
                csv_file = csv.reader(card_file, delimiter=';')

                for line in csv_file:
                    card_name = line[1]
                    self.create_card(card_name, 'black')

            else:
                for line in card_file:
                    card_name = line[:-1]

                    self.create_card(card_name, 'black')

    def create_card(self, card_name, card_type):
        card = Card(name=card_name, card_type=card_type, created_by=None)
        db.session.add(card)
        db.session.commit()

        association = CardAssociation(
            card_id=card.id, collection_id=self.id)
        db.session.add(association)
        db.session.commit()

    @property
    def count_white_cards(self):
        return sum(card.card_type == 'white' for card in self.cards)

    @property
    def count_black_cards(self):
        return sum(card.card_type == 'black' for card in self.cards)

    def set_owner(self, user_id):
        new_ownership = OwnedCollection(user_id=user_id, collection_id=self.id)

        db.session.add(new_ownership)
        db.session.commit()
