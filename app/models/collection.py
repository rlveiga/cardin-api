from app import db

class Collection(db.Model):
    __tablename__ = 'collections'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    value = db.Column(db.Integer)
    # owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    cards = db.relationship('Card', backref='collection')