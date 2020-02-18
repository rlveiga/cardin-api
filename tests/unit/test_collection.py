import json

import pytest

from app import db
from app.models.card import Card, CardAssociation
from app.models.collection import Collection


@pytest.fixture
def init_cards_collections_db():
  # Default collections
  default_collection1 = Collection(name="My cards", created_by=1, is_deletable=False)
  default_collection2 = Collection(name="My cards", created_by=2, is_deletable=False)
  
  # User 1's collections
  collection1 = Collection(name='Test collection', created_by=1)
  collection2 = Collection(name="Deletable collection", created_by=1)

  # User 2's collections
  collection3 = Collection(name="Steve's collection", created_by=2)

  collections = [
      default_collection1,
      default_collection2,
      collection1,
      collection2,
      collection3
  ]

  db.session.add_all(collections)
  db.session.commit()

  # Test cards
  # User 1's cards
  card1 = Card(card_type='black', name='I am starting to feel', created_by=1)
  card2 = Card(card_type='white', name='Deletable card', created_by=1)

  # User 2's cards
  card3 = Card(card_type='white', name='Social justice', created_by=2)
  card4 = Card(card_type='white', name='Undeletable card', created_by=2)

  cards = [
    card1,
    card2,
    card3,
    card4
  ]

  db.session.add_all(cards)
  db.session.commit()

  # Test card associations
  # User 1's card associations
  card_association1 = CardAssociation(card_id=card1.id, collection_id=collection1.id)
  card_association2 = CardAssociation(card_id=card2.id, collection_id=collection1.id)

  # User 2's card associations
  card_association3 = CardAssociation(card_id=card3.id, collection_id=collection3.id)

  card_associations = [
    card_association1,
    card_association2,
    card_association3
  ]

  db.session.add_all(card_associations)
  db.session.commit()

  yield db

  db.session.close()
  db.drop_all()

def test_get_collection_info(test_client, init_db, init_cards_collections_db, token):
  response = test_client.get('/collections/3', headers={'access-token': token})

  data = json.loads(response.data)

  assert response.status_code == 200

  assert type(data['collection']['cards']) is list
  assert data['collection']['cards'][0]['name'] == 'I am starting to feel'

def test_get_unexisting_collection_info(test_client, init_db, init_cards_collections_db, token):
  response = test_client.get('/collections/42', headers={'access-token': token})

  data = json.loads(response.data)

  assert response.status_code == 404

  assert data['message'] == 'Collection not found'

def test_get_unauthorized_collection_info(test_client, init_db, init_cards_collections_db, token):
  response = test_client.get('/collections/5', headers={'access-token': token})

  data = json.loads(response.data)

  assert response.status_code == 403

  assert data['message'] == 'You do not own this collection'

def test_get_cards_from_collection(test_client, init_db, init_cards_collections_db, token):
  response = test_client.get('/collections/3/cards', headers={'access-token': token})

  data = json.loads(response.data)

  assert response.status_code == 200

  assert type(data['cards']) is list

def test_get_cards_from_unexisting_collection(test_client, init_db, init_cards_collections_db, token):
  response = test_client.get('/collections/42/cards', headers={'access-token': token})

  data = json.loads(response.data)

  assert response.status_code == 404

  assert data['message'] == 'Collection not found'

def test_get_cards_from_unauthorized_collection(test_client, init_db, init_cards_collections_db, token):
  response = test_client.get('/collections/5/cards', headers={'access-token': token})

  data = json.loads(response.data)

  assert response.status_code == 401

  assert data['message'] == 'You do not own this collection'

def test_create_collection(test_client, init_db, init_cards_collections_db, token):
  response = test_client.post('/collections/', json=dict(name='Random collection'), headers={'access-token': token})

  data = json.loads(response.data)

  assert response.status_code == 201

  assert type(data['collection']) == dict
  assert data['collection']['data']['name'] == 'Random collection'
  assert type(data['collection']['cards']) == list

def test_delete_collection(test_client, init_db, init_cards_collections_db, token):
  response = test_client.delete('/collections/4', headers={'access-token': token})

  data = json.loads(response.data)

  assert response.status_code == 200

  assert data['message'] == 'Collection deleted'
  assert data['collection'] == {}

def test_delete_unexisting_collection(test_client, init_db, init_cards_collections_db, token):
  response = test_client.delete('/collections/42', headers={'access-token': token})

  data = json.loads(response.data)

  assert response.status_code == 404

  assert data['message'] == 'Collection not found'

def test_delete_unauthorized_collection(test_client, init_db, init_cards_collections_db, token):
  response = test_client.delete('/collections/5', headers={'access-token': token})

  data = json.loads(response.data)

  assert response.status_code == 401

  assert data['message'] == 'You do not own this collection'
