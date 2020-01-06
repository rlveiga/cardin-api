from app.models.room import Room

import json

def test_reset_state(init_db):
    room = Room.query.filter_by(id=1).one()

    room.reset_state()

    state = json.loads(room.state)

    assert type(state) == dict
    assert state['game_state'] == 'Zero'
    assert state['deck'] == []
    assert state['hands'] == [[]] * 4
    assert state['turn'] == 0
    assert state['scores'] == [0] * 4

def test_load_state(init_db):
    room = Room.query.filter_by(id=1).one()

    state = room.load_state()

    assert type(state) == dict
    assert state['game_state'] == 'Zero'
    assert state['deck'] == []
    assert state['hands'] == [[]] * 4
    assert state['turn'] == 0
    assert state['scores'] == [0] * 4

def test_create_deck(init_db):
    pass

def test_add_player(init_db):
    pass

def test_remove_player(init_db):
    pass