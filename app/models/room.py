from app import db
from app.models.schemas import user_share_schema, users_share_schema, room_share_schema
from datetime import datetime

class Card(db.Model):
    __tablename__ = 'cards'

    id = db.Column(db.Integer, primary_key=True)
    card_type = db.Column(db.String(16), nullable=False)
    card_text = db.Column(db.String(64), nullable=False)
    # collection = db.Column(db.Integer, db.ForeignKey('collections.id'))

class WhiteGameCard(db.Model):
    __tablename__ = 'white_game_cards'

    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('cards.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)

class BlackGameCard(db.Model):
    __tablename__ = 'black_game_cards'

    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('cards.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)

class Association(db.Model):
    __tablename__ = 'association'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    date_joined = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)

class Room(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(64), default='active')
    created_by = db.Column(db.Integer)
    code = db.Column(db.String(5))
    white_cards = db.relationship("WhiteGameCard", backref='room')
    black_cards = db.relationship("BlackGameCard", backref='room')
    users = db.relationship("User", secondary='association')

    def create_deck(self, cards):
        for card in cards:
            if(card.card_type == 'black'):
                new_black_card = BlackGameCard(card_id=card.id, room_id=self.id)

                db.session.add(new_black_card)

            else:
                new_white_card = WhiteGameCard(card_id=card.id, room_id=self.id)

                db.session.add(new_white_card)

            db.session.commit()

    #shuffle    s and distributes cards
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