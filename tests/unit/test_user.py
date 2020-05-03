import json

from app.models.user import User

def test_create_user(test_client, init_db):
    response = test_client.post('/auth/register', json=dict(username='test_user', password='abc123'))

    data = json.loads(response.data)

    assert response.status_code == 201

    assert data['message'] == 'User created'
    assert data['user']['source'] == 'cardin'

def test_create_user_fail(test_client, init_db):
    response = test_client.post('/auth/register', json=dict(username='test_user', password='abc123'))

    data = json.loads(response.data)

    assert response.status_code == 409

    assert data['message'] == 'Username is taken'

def test_login_success(test_client, init_db):
    response = test_client.post('/auth/login', json=dict(username='test_user', password='abc123'))
    
    data = json.loads(response.data)

    assert response.status_code == 200
    
    assert type(data['token']) is str

def test_login_fail(test_client, init_db):
    response = test_client.post('/auth/login', json=dict(username='test_user', password='abcd1234'))

    data = json.loads(response.data)

    assert response.status_code == 401

def test_login_not_found(test_client, init_db):
    response = test_client.post('/auth/login', json=dict(username='mark', password='abc123'))

    data = json.loads(response.data)

    assert response.status_code == 404

def test_get_user_collections(test_client, init_db, token):
    response = test_client.get('/collections/', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200

    assert type(data['collections']) is list
    assert type(data['collections'][0]) is dict
    assert data['collections'][0]['name'] == 'Minhas cartas'
    assert type(data['collections'][0]['black_card_count']) is int
    assert type(data['collections'][0]['white_card_count']) is int

def test_get_user_cards(test_client, init_db, token):
    response = test_client.get('/cards/', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200

    assert type(data['cards']) is list
    assert type(data['cards'][0]) is dict