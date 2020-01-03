import json

from app.models.card import Card
from app.models.collection import Collection

def test_get_collection(test_client, init_db, token):
    pass

def test_create_collection(test_client, init_db, token):
    response = test_client.post('/collection', json=dict(name='Collection test'), headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 201
    assert data['message'] == 'Collection created'
    assert type(data['collection']) == dict
    assert data['collection']['name'] == 'Collection test'
    assert type(data['collection']['cards']) == dict

def test_add_to_collection(test_client, init_db, token):
    response = test_client.put('/collection/1', json=dict(card_type='white', card_text='Daft Punk'), headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200
    assert type(data['collection']['cards']) == list
    assert data['collection']['cards'][0]['card_type'] == 'white'
    assert data['collection']['cards'][0]['card_text'] == 'Daft Punk'

def test_add_to_unexisting_collection(test_client, init_db, token):
    pass

def test_add_unexisting_card_to_collection(test_client, init_db, token):
    pass

def test_remove_from_collection(test_client, init_db, token):
    collection = Collection.query.filter_by(id=1).one()

    assert len(collection.cards) == 2

    collection.remove_card(collection.cards[0])

    assert collection.cards.length == 0
