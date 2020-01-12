from app.models.room import Room

import json

def test_reset_game(test_client, init_db):
    room = Room.query.filter_by(id=1).one()

    room.reset_game()

    data = json.loads(room.data)

    assert type(data) == dict
    assert data['state'] == 'Zero'
    assert data['deck'] == []
    assert data['hands'] == [[]] * 4
    assert data['scores'] == [0] * 4

def test_load_game(test_client, init_db):
    room = Room.query.filter_by(id=1).one()

    data = room.load_game()

    assert type(data) == dict
    assert data['state'] == 'Zero'
    assert data['deck'] == []
    assert data['hands'] == [[]] * 4
    assert data['scores'] == [0] * 4

def test_create_deck(test_client, init_db):
    pass    

def test_add_player(test_client, init_db):
    pass

def test_remove_player(test_client, init_db):
    pass