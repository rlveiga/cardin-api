import json
from app.models.room import Room

def test_create_room(test_client, init_db, token):
    response = test_client.post('/rooms', json=dict(code='abcde'), headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200
    assert type(data['room']) == dict
    assert data['room']['data']['code'] == 'abcde'
    assert data['room']['users'][0]['name'] == 'rodrigo'

def test_join_room(test_client, init_db, token):
    response = test_client.post('/rooms/2', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['room']['data']['id'] == 2
    assert data['room']['users'][0]['name'] == 'rodrigo'

def test_join_unexisting_room(test_client, init_db, token):
    response = test_client.post('/rooms/42', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 404
    assert data['message'] == 'Room not found'  

def test_get_room_players(test_client, init_db, token):
    response = test_client.get('/rooms/1', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['users'][0]['name']== 'rodrigo'
    
def test_get_unexisting_room_players(test_client, init_db, token):
    response = test_client.get('/rooms/42', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 404
    assert data['message'] == 'Room not found'

def test_leave_room(test_client, init_db, token):
    response = test_client.delete('/rooms/2', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['success'] == True

def test_leave_room_not_allowed(test_client, init_db, token):
    response = test_client.delete('/rooms/2', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 404
    assert data['success'] == False
    assert data['message'] == 'You do not belong to this room'

def test_leave_unexisting_room(test_client, init_db, token):
    response = test_client.delete('/rooms/45', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 404
    assert data['success'] == False
    assert data['message'] == 'Room not found'