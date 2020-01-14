import json
from app.models.room import Room

def test_get_user_room(test_client, init_db, token):
    response = test_client.get('/rooms/', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200
    
    assert type(data['room']) is dict
    
def test_create_room(test_client, init_db, token):
    response = test_client.post('/rooms/', json=dict(code='abcde'), headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200
    assert type(data['room']) == dict
    assert data['room']['data']['code'] == 'abcde'
    assert data['room']['users'][0]['username'] == 'rodrigo'

def test_join_room(test_client, init_db, token):
    response = test_client.post('/rooms/test2', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['room']['data']['id'] == 2
    assert data['room']['users'][0]['username'] == 'rodrigo'

def test_join_unexisting_room(test_client, init_db, token):
    response = test_client.post('/rooms/test3', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 404
    assert data['message'] == 'Room not found'  

def test_get_room_info(test_client, init_db, token):
    response = test_client.get('/rooms/test2', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['room']['data']['code'] == 'test2'
    assert data['room']['users'][0]['data']['username']== 'rodrigo'
    
def test_get_unexisting_room_players(test_client, init_db, token):
    response = test_client.get('/rooms/test3', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 404
    assert data['message'] == 'Room not found'

def test_leave_room(test_client, init_db, token):
    response = test_client.delete('/rooms/2', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200

def test_leave_room_not_allowed(test_client, init_db, token):
    response = test_client.delete('/rooms/2', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200

def test_leave_unexisting_room(test_client, init_db, token):
    response = test_client.delete('/rooms/45', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 404
    assert data['message'] == 'Room not found'