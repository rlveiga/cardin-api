from app import db
from datetime import datetime


class CardAssociation(db.Model):
    __tablename__ = 'card_association'

    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('cards.id'))
    collection_id = db.Column(db.Integer, db.ForeignKey('collections.id'))
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)


class Card(db.Model):
    __tablename__ = 'cards'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    card_type = db.Column(db.String(16), nullable=False)
    slots = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    created_by = db.Column(db.Integer)
    collections = db.relationship("Collection", secondary='card_association')

    def __init__(self, name, card_type, created_by):
        self.name = self.format_name(name, card_type)
        self.card_type = card_type
        self.created_by = created_by

        self.set_empty_slots()

    def set_empty_slots(self):
        slots = 0
        words = self.name.split(' ')

        for e in words:
            if '____' in e:
                slots += 1

        # Set slots equal to one even if there are no blank spaces
        if slots == 0:
            slots = 1

        self.slots = slots

    def format_name(self, name, card_type):
        if card_type == 'white':
            return name

        words = name.split(' ')

        for i, e in enumerate(words):
            if '_' in e:
                count = 0

                for c in e[1:]:
                    if c == '_':
                        count += 1

                words[i] = '____' + e[count+1:]

        formatted = ' '.join(words)
        return formatted
