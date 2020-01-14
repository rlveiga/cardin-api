import json

def test_create_card(test_client, init_db, token):
    response = test_client.post('/cards/', json=dict(card_type='black', name='Something clever'), headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200

    assert data['message'] == 'Card created'
    assert type(data['card']) == dict
    assert data['card']['card_type'] == 'black'
    assert data['card']['name'] == 'Something clever'
    assert data['card']['created_by'] == 1

def test_delete_card(test_client, init_db, token):
    response = test_client.delete('/cards/3', headers={'access-token': token})

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
    response = test_client.delete('/cards/4', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 401

    assert data['message'] == 'You do not own this card'

def test_add_to_collection(test_client, init_db, token):
    response = test_client.put('/cards/1/add_collection/4', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200

    assert data['message'] == 'Card added to collection'
    assert data['card']['collection_id'] == 4

def test_add_to_unexisting_collection(test_client, init_db, token):
    pass
    # response = test_client.put('/cards/1/add_collection/42', headers={'access-token': token})

    # data = json.loads(response.data)

    # assert response.status_code == 404

    # assert data['message'] == 'Collection not found'

def test_add_unexisting_card_to_collection(test_client, init_db, token):
    pass
    # response = test_client.put('/cards/42/add_collection/1', headers={'access-token': token})

    # data = json.loads(response.data)

    # assert response.status_code == 404

    # assert data['message'] == 'Card not found'

def test_add_to_unauthorized_collection(test_client, init_db, token):
    response = test_client.put('/cards/1/add_collection/2', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 401

    assert data['message'] == 'You do not own this collection'

def test_remove_from_collection(test_client, init_db, token):
    pass

def test_remove_from_unexisting_collection(test_client, init_db, token):
    pass

def test_remove_unexisting_card_from_collection(test_client, init_db, token):
    pass

def test_remove_from_unauthorized_collection(test_client, init_db, token):
    pass