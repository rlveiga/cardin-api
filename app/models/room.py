from app import db
from app.models.schemas import user_share_schema, users_share_schema, room_share_schema, cards_share_schema
from datetime import datetime
from enum import Enum

class Card(db.Model):
    __tablename__ = 'cards'

    id = db.Column(db.Integer, primary_key=True)
    card_type = db.Column(db.String(16), nullable=False)
    card_text = db.Column(db.String(64), nullable=False)
    # collection = db.Column(db.Integer, db.ForeignKey('collections.id'))

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

class CardUsage(db.Model):
    __tablename__ = 'card_usage'

    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('cards.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))

class Association(db.Model):
    __tablename__ = 'association'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    date_joined = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)

class GameState(Enum):
    Zero = 0
    Choosing = 1
    Judging = 2
    Results = 3

class Room(db.Model):
    __tablename__ = 'rooms'

    game_state = GameState.Zero

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(64), default='active')
    created_by = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    code = db.Column(db.String(12))
    deck = db.relationship("Card", secondary='card_usage')
    # white_cards = db.relationship("WhiteGameCard", backref='room')
    # black_cards = db.relationship("BlackGameCard", backref='room')
    users = db.relationship("User", secondary='association')

    def create_deck(self, cards):
        for card in cards:
            db.session.add(CardUsage(card_id=card.id, room_id=self.id))

        db.session.commit()

    #shuffles and distributes cards
    def shuffle_deck(self, user_id):
        pass        

    def add_player(self, user_id):
        if len(self.users) < 4:
            new_join = Association(user_id=user_id, room_id=self.id)

            db.session.add(new_join)
            db.session.commit()

            return {
                'success': True,
                'room': {
                    'data': room_share_schema.dump(self),
                    'users': users_share_schema.dump(self.users)
                }
            }

        else:
            return {
                'success': False,
                'message': 'Room is full'
            }
    
    def remove_player(self, user_id):
        for u in self.users:
            if u.id == user_id:
                association = Association.query.filter_by(room_id=self.id, user_id=user_id).first()

                db.session.delete(association)
                db.session.commit()
                
                return {
                    'success': True,
                    'message': 'User removed'
                }

        else:
            return {
                'success': False,
                'message': 'User is not in this room'
            }