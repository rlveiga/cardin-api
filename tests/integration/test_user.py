import json

from app.models.user import User

def test_login_success(test_client, init_db):
    response = test_client.post('/auth/login', json=dict(username='rodrigo', password='abc123'))
    
    data = json.loads(response.data)

    assert data['success'] == True
    assert response.status_code == 200
    assert type(data['token']) is str

def test_login_fail(test_client, init_db):
    response = test_client.post('/auth/login', json=dict(username='rodrigo', password='abcd1234'))

    data = json.loads(response.data)

    assert data['success'] == False
    assert response.status_code == 200

def test_login_not_found(test_client, init_db):
    response = test_client.post('/auth/login', json=dict(username='mark', password='abc123'))

    data = json.loads(response.data)

    assert data['success'] == False
    assert response.status_code == 404

def test_get_current_room(test_client, init_db, token):
    response = test_client.get('/rooms', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['success'] == True
    assert type(data['room']) is dict