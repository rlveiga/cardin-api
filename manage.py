from app import app, db, socketio
from app.models.user import User
from app.models.room import Room, RoomAssociation
from app.models.card import Card, CardAssociation
from app.models.collection import Collection, OwnedCollections

import flask
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand 
from flask_socketio import SocketIO

import os, csv, time

manager = Manager(app)
Migrate = Migrate(app, db)

def make_shell_context():
	return dict(app=app, db=db, User=User, Card=Card, Collection=Collection, OwnedCollections=OwnedCollections, Room=Room, RoomAssociation=RoomAssociation)

@manager.command
def run():
  socketio.run(app)

# Creates deck from CSV file and adds them to collection
@manager.command
def create_deck(folder_path, collection_name):
  white_cards = []
  black_cards = []

  white_cards_path = f"./{folder_path}/white_cards.csv"
  black_cards_path = f"./{folder_path}/black_cards.csv"

  new_collection = Collection(name=collection_name, editable=False)
  db.session.add(new_collection)
  db.session.commit()

  with open(white_cards_path) as csv_file:
    white_cards_reader = csv.reader(csv_file, delimiter=';')

    for row in white_cards_reader:
      new_card = Card(name=row[1], card_type='white')
      db.session.add(new_card)
      db.session.commit()

      new_association = CardAssociation(card_id=new_card.id, collection_id=new_collection.id)

      db.session.add(new_association)
      db.session.commit()

  with open(black_cards_path) as csv_file:
    black_cards_reader = csv.reader(csv_file, delimiter=';')

    for row in black_cards_reader:
      new_card = Card(name=row[1], card_type='black')

      db.session.add(new_card)
      db.session.commit()

      new_association = CardAssociation(card_id=new_card.id, collection_id=new_collection.id)

      db.session.add(new_association)
      db.session.commit()

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
	manager.run()