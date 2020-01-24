from app import db
from datetime import datetime

class Collection(db.Model):
    __tablename__ = 'collections'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    cards = db.relationship("Card", secondary='card_association')
    is_deletable = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def get_cards(self):
        pass