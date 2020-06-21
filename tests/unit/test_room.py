import json

from app.models.room import Room, RoomAssociation
from app.models.collection import Collection
from app.models.schemas import collection_share_schema


def test_get_room_info(test_client, init_db, token):
    response = test_client.get(
        '/rooms/room1', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200

    assert data['data']['code'] == 'room1'
    assert data['data']['status'] == 'waiting'
    assert type(data['data']['user_list']) is list


def test_join_unexisting_room(test_client, init_db, token):
    response = test_client.post(
        '/rooms/four2', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 404

    assert data['message'] == 'Room not found'


def test_join_active_room(test_client, init_db, token):
    room = Room.query.filter_by(status='active').first()

    response = test_client.post(
        f"/rooms/{room.code}", headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 422

    assert data['message'] == 'Room is currently hosting a game'


def test_join_room(test_client, init_db, token):
    response = test_client.post(
        '/rooms/room1', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['data']['code'] == 'room1'
    assert data['data']['collection']['name'] == 'Minhas cartas'
    assert type(data['data']['collection']['black_card_count']) is int
    assert type(data['data']['collection']['white_card_count']) is int
    assert len(data['data']['users']) == 2


def test_join_another_room(test_client, init_db, token):
    response = test_client.post(
        '/rooms/room3', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['data']['code'] == 'room3'
    assert data['data']['collection']['name'] == 'Minhas cartas'
    assert len(data['data']['users']) == 2


def test_leave_room(test_client, init_db, token):
    response = test_client.delete(
        '/rooms/room3', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200


def test_leave_room_not_allowed(test_client, init_db, token):
    response = test_client.delete(
        '/rooms/room1', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 422

    assert data['message'] == 'User is not in this room'


def test_leave_unexisting_room(test_client, init_db, token):
    response = test_client.delete(
        '/rooms/four2', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 404
    assert data['message'] == 'Room not found'


def test_create_existing_room(test_client, init_db, token):
    room = Room.query.filter_by(code="room1").first()
    print('room status: ', room.status)

    collection = Collection.query.first()

    response = test_client.post(
        '/rooms/', json=dict(code='room1', collection_id=collection.id), headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 403
    assert data['message'] == "Room 'room1' is already in use"


def test_create_room_unexisting_collection(test_client, init_db, token):
    response = test_client.post(
        '/rooms/', json=dict(code='abcde', collection_id=42), headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 404
    assert data['message'] == 'Collection not found'


def test_create_room(test_client, init_db, token):
    collection = Collection.query.first()

    response = test_client.post(
        '/rooms/', json=dict(code='abcde', collection_id=collection.id), headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['data']['status'] == 'waiting'
    assert data['data']['collection']['name'] == 'Minhas cartas'
    assert type(data['data']['collection']['black_card_count']) is int
    assert type(data['data']['collection']['white_card_count']) is int
    assert data['data']['users'][0]['name'] == 'user_1'
    assert data['data']['game'] is None


def test_create_another_room(test_client, init_db, token):
    collection = Collection.query.first()

    response = test_client.post(
        '/rooms/', json=dict(code='abcdf', collection_id=collection.id), headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['data']['status'] == 'waiting'
    assert data['data']['collection']['name'] == 'Minhas cartas'
    assert data['data']['users'][0]['name'] == 'user_1'
    assert data['data']['game'] is None
