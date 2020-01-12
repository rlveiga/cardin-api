import json

from app.models.user import User

def test_login_success(test_client, init_db):
    response = test_client.post('/auth/login', json=dict(username='rodrigo', password='abc123'))
    
    data = json.loads(response.data)

    assert response.status_code == 200
    
    assert type(data['token']) is str

def test_login_fail(test_client, init_db):
    response = test_client.post('/auth/login', json=dict(username='rodrigo', password='abcd1234'))

    data = json.loads(response.data)

    assert response.status_code == 401

def test_login_not_found(test_client, init_db):
    response = test_client.post('/auth/login', json=dict(username='mark', password='abc123'))

    data = json.loads(response.data)

    assert response.status_code == 404

def test_get_user_room(test_client, init_db, token):
    response = test_client.get('/rooms', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200
    
    assert type(data['room']) is dict

def test_get_user_collections(test_client, init_db, token):
    response = test_client.get('/collections', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200

    assert type(data['collections']) is list
    assert type(data['collections'][0]) is dict

    assert type(data['collections'][0]['data']) is dict
    assert type(data['collections'][0]['cards']) is list

def test_get_user_cards(test_client, init_db, token):
    response = test_client.get('/cards', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200

    assert type(data['cards']) is list
    assert type(data['cards'][0]) is dict