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
    name = db.Column(db.String(64), nullable=False)
    card_type = db.Column(db.String(16), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    created_by = db.Column(db.Integer)
    collections = db.relationship("Collection", secondary='card_association')