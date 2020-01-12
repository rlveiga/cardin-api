import json

from app.models.card import Card
from app.models.collection import Collection

def test_create_collection(test_client, init_db, token):
    response = test_client.post('/collections', json=dict(name='Random collection'), headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 201
    
    assert type(data['collection']) == dict
    assert data['collection']['data']['name'] == 'Random collection'
    assert type(data['collection']['cards']) == list

def test_delete_collection(test_client, init_db, token):
    response = test_client.delete('/collections/1', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200

    assert data['message'] == 'Collection deleted'

def test_delete_unexisting_collection(test_client, init_db, token):
    response = test_client.delete('/collections/42', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 404

    assert data['message'] == 'Collection not found'

def test_delete_unauthorized_collection(test_client, init_db, token):
    pass

def test_add_to_collection(test_client, init_db, token):
    pass
    # response = test_client.put('/collections/1', json=dict(card_type='white', name='Daft Punk'), headers={'access-token': token})

    # data = json.loads(response.data)

    # assert response.status_code == 200
    # assert type(data['collection']['cards']) == list
    # assert data['collection']['cards'][0]['card_type'] == 'white'
    # assert data['collection']['cards'][0]['name'] == 'Daft Punk'

def test_add_to_unexisting_collection(test_client, init_db, token):
    pass

def test_add_unexisting_card_to_collection(test_client, init_db, token):
    pass

def test_add_card_to_unauthorized_collection(test_client, init_db, token):
    pass

def test_remove_from_collection(test_client, init_db, token):
    pass

def test_remove_from_unexisting_collection(test_client, init_db, token):
    pass

def test_remove_unexisting_card_from_collection(test_client, init_db, token):
    pass

def test_remove_from_unauthorized_collection(test_client, init_db, token):
    pass

def test_get_cards_from_collection(test_client, init_db, token):
    pass

def test_get_cards_from_unexisting_collection(test_client, init_db, token):
    pass

def test_get_cards_from_unauthorized_collection(test_client, init_db, token):
    pass