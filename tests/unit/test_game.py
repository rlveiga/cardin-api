from app.models.room import Room
from app.models.collection import Collection
from app.models.schemas import collection_share_schema

import random


def test_init_room(test_client, init_game_db):
    room = Room.query.first()
    collection = Collection.query.first()

    room.init_room(collection)

    game_data = room.load_game()

    assert game_data['state'] == 'Zero'
    assert game_data['collection'] == collection_share_schema.dump(collection)
    assert type(game_data['all_cards']) is list
    assert type(game_data['white_cards']) is list
    assert type(game_data['black_cards']) is list
    assert game_data['discarded_cards'] == []
    assert game_data['table_card'] is None
    assert game_data['hands'] == [{
        'user_id': 1,
        'cards': []
    }]
    assert game_data['selected_cards'] == [{
        'user_id': 1,
        'cards': []
    }]
    assert game_data['scores'] == [{
        'user_id': 1,
        'score': 0
    }]
    assert game_data['czar_id'] is None
    assert game_data['round_winner'] is None


def test_add_player(test_client, init_game_db):
    room = Room.query.first()

    room.add_user(2)

    game_data = room.load_game()

    assert game_data['hands'] == [{
        'user_id': 1,
        'cards': []
    }, {
        'user_id': 2,
        'cards': []
    }]
    assert game_data['selected_cards'] == [{
        'user_id': 1,
        'cards': []
    }, {
        'user_id': 2,
        'cards': []
    }]
    assert game_data['scores'] == [{
        'user_id': 1,
        'score': 0
    }, {
        'user_id': 2,
        'score': 0
    }]


def test_distribute_cards(test_client, init_game_db):
    room = Room.query.first()

    room.distribute_cards(7)

    game_data = room.load_game()

    assert game_data['hands'][0]['user_id'] == 1
    assert len(game_data['hands'][0]['cards']) == 7
    assert len(game_data['discarded_cards']) == 14


def test_pick_table_card(test_client, init_game_db):
    room = Room.query.first()

    room.pick_table_card()

    game_data = room.load_game()

    assert game_data['table_card'] is not None
    assert len(game_data['discarded_cards']) == 15


def test_pick_czar(test_client, init_game_db):
    room = Room.query.first()

    room.pick_czar()

    game_data = room.load_game()

    assert type(game_data['czar_id']) is int


def test_set_cards_for_user(test_client, init_game_db):
    room = Room.query.first()

    game_data = room.load_game()

    room.set_cards_for_user(1, [game_data['hands'][0]['cards'][0]])
    room.set_cards_for_user(2, [game_data['hands'][1]['cards'][0]])

    game_data = room.load_game()

    assert len(game_data['hands'][0]['cards']) == 6
    assert len(game_data['hands'][1]['cards']) == 6

    assert len(game_data['selected_cards'][0]['cards']) == 1
    assert len(game_data['selected_cards'][1]['cards']) == 1


def test_pick_winner(test_client, init_game_db):
    room = Room.query.first()

    game_data = room.load_game()

    winner_id = game_data['hands'][0]['user_id']

    room.pick_winner(winner_id)

    game_data = room.load_game()

    assert game_data['round_winner'] == winner_id
    assert game_data['scores'][0]['score'] == 1


def test_start_new_round(test_client, init_game_db):
    room = Room.query.first()

    room.start_new_round()

    game_data = room.load_game()

    assert game_data['table_card'] is None
    assert game_data['czar_id'] is None
    assert game_data['round_winner'] is None
    assert len(game_data['hands'][0]['cards']) == 7
    assert len(game_data['hands'][1]['cards']) == 7
    assert len(game_data['selected_cards'][0]['cards']) == 0
    assert len(game_data['selected_cards'][1]['cards']) == 0

def test_remove_user(test_client, init_game_db):
    room = Room.query.first()

    room.remove_user(2)

    game_data = room.load_game()

    assert len(game_data['hands']) == 1
    assert len(game_data['scores']) == 1
    assert len(game_data['selected_cards']) == 1
