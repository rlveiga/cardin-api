from app.models.collection import Collection
from app.models.card import Card, CardAssociation
from app import db

import csv

def create_deck(folder_path, collection_name):
  white_cards = []
  black_cards = []

  white_cards_path = f"./decks/{folder_path}/white_cards.csv"
  black_cards_path = f"./decks/{folder_path}/black_cards.csv"

  new_collection = Collection(name=collection_name, editable=False)
  db.session.add(new_collection)
  db.session.commit()

  with open(white_cards_path) as csv_file:
    white_cards_reader = csv.reader(csv_file, delimiter=';')

    for row in white_cards_reader:
      new_card = Card(name=row[1], card_type='white', created_by=None)
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