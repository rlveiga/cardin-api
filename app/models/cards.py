# from app import db

# class Card(db.Model):
#     __tablename__ = 'cards'

#     id = db.Column(db.Integer, primary_key=True)
#     card_type = db.Column(db.String(16), nullable=False)
#     card_text = db.Column(db.String(64), nullable=False)
#     # collection = db.Column(db.Integer, db.ForeignKey('collections.id'))

# class WhiteGameCard(db.Model):
#     __tablename__ = 'white_game_cards'

#     id = db.Column(db.Integer, primary_key=True)
#     card_id = db.Column(db.Integer, db.ForeignKey('cards.id'), nullable=False)
#     room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)

# class BlackGameCard(db.Model):
#     __tablename__ = 'black_game_cards'

#     id = db.Column(db.Integer, primary_key=True)
#     card_id = db.Column(db.Integer, db.ForeignKey('cards.id'), nullable=False)
#     room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
