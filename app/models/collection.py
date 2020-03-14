from app import db
from datetime import datetime

class OwnedCollection(db.Model):
  __tablename__ = 'owned_collections'

  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  collection_id = db.Column(db.Integer, db.ForeignKey('collections.id'))
  created_at = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)

class Collection(db.Model):
  __tablename__ = 'collections'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(20), nullable=False)
  cards = db.relationship('Card', secondary='card_association')
  owners = db.relationship('User', secondary='owned_collections')
  editable = db.Column(db.Boolean, default=True)
  created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
  created_by = db.Column(db.Integer)

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