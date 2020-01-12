import json

def test_create_card(test_client, init_db, token):
    response = test_client.post('/card', json=dict(card_type='black', name='Something clever'), headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['message'] == 'Card created'
    assert type(data['card']) == dict
    assert data['card']['card_type'] == 'black'
    assert data['card']['name'] == 'Something clever'

    assert type(data['card']['created_by']) == dict
    assert data['card']['created_by']['id'] == 1

def test_add_to_collection(test_client, init_db, token):
    pass

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