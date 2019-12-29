from app import db

class Card(db.Model):
    __tablename__ = 'cards'

    id = db.Column(db.Integer, primary_key=True)
    card_text = db.Column(db.String(64), nullable=False)
    card_type = db.Column(db.String(16), nullable=False)
    collection_id = db.Column(db.Integer, db.ForeignKey('collections.id'))
    collection = db.relationship('Collection')