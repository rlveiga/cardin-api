import json

import pytest

from app import db
from app.models.card import Card, CardAssociation
from app.models.collection import Collection


def test_create_card(test_client, init_db, token):
    collection = Collection.query.filter_by(name='collection_1').first()

    response = test_client.post('/cards/', json=dict(card_type='black', name='Where is ____?',
                                                     collection_id=collection.id), headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200

    assert data['message'] == 'Card created'
    assert type(data['card']) == dict
    assert data['card']['card_type'] == 'black'
    assert data['card']['slots'] == 1
    assert data['card']['name'] == 'Where is ____?'
    assert data['card']['created_by'] == 1
    assert type(data['card']['collections']) == list
    assert data['card']['collections'][0]['name'] == 'Minhas cartas'
    assert data['card']['collections'][1]['name'] == 'collection_1'
    assert data['card']['collections'][0]['created_by'] == 1


def test_get_card_info(test_client, init_db, token):
    card = Card.query.filter_by(created_by=1, name='Where is ____?').first()

    response = test_client.get(f"/cards/{card.id}", headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['card']['name'] == 'Where is ____?'
    assert data['card']['card_type'] == 'black'
    assert len(data['collections']) == 2


def test_get_unexisting_card_info(test_client, init_db, token):
    response = test_client.get('/cards/42', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 404


def test_get_forbidden_card_info(test_client, init_db, token):
    card = Card.query.filter_by(created_by=2).first()

    response = test_client.get(f"/cards/{card.id}", headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 403

def test_delete_card(test_client, init_db, token):
    card = Card.query.filter_by(created_by=1, name='Where is ____?').first()

    response = test_client.delete(f"/cards/{card.id}", headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200

    assert data['message'] == 'Card deleted'
    assert data['card'] == {}

def test_delete_unexisting_card(test_client, init_db, token):
    response = test_client.delete('/cards/42', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 404

    assert data['message'] == 'Card not found'

def test_delete_unauthorized_card(test_client, init_db, token):
    card = Card.query.filter_by(created_by=2).first()

    response = test_client.delete(f"/cards/{card.id}", headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 403

    assert data['message'] == 'You do not own this card'
