from app import db
from datetime import datetime

class Card(db.Model):
    __tablename__ = 'cards'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    card_type = db.Column(db.String(16), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    created_by = db.Column(db.Integer, nullable=False)
    collection_id = db.Column(db.Integer, db.ForeignKey('collections.id'))