import json

from app.models.card import Card
from app.models.collection import Collection

def test_create_collection(test_client, init_db, token):
    response = test_client.post('/collections/', json=dict(name='Random collection'), headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 201
    
    assert type(data['collection']) == dict
    assert data['collection']['data']['name'] == 'Random collection'
    assert type(data['collection']['cards']) == list

def test_delete_collection(test_client, init_db, token):
    response = test_client.delete('/collections/3', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200

    assert data['message'] == 'Collection deleted'
    assert data['collection'] == {}

def test_delete_unexisting_collection(test_client, init_db, token):
    response = test_client.delete('/collections/42', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 404

    assert data['message'] == 'Collection not found'

def test_delete_unauthorized_collection(test_client, init_db, token):
    response = test_client.delete('/collections/2', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 401

    assert data['message'] == 'You do not own this collection'

def test_get_cards_from_collection(test_client, init_db, token):
    response = test_client.get('/collections/1/cards', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200
    
    assert type(data['cards']) is list

def test_get_cards_from_unexisting_collection(test_client, init_db, token):
    response = test_client.get('/collections/42/cards', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 404
    
    assert data['message'] == 'Collection not found'

def test_get_cards_from_unauthorized_collection(test_client, init_db, token):
    response = test_client.get('/collections/2/cards', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 401
    
    assert data['message'] == 'You do not own this collection'