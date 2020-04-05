from app.models.room import Room
from app.models.user import User
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
    assert game_data['players'] == [{
        'data': {
            'username': 'rodrigo',
            'id': 1
        },
        'hand': [],
        'score': 0,
        'is_ready': False
    }]
    assert game_data['selected_cards'] == []
    assert game_data['czar_id'] is None
    assert game_data['round_winner'] is None
    assert game_data['all_players_ready'] == False


def test_add_user(test_client, init_game_db):
    room = Room.query.first()
    user = User.query.filter_by(id=2).first()

    room.add_user(user)

    game_data = room.load_game()

    assert game_data['players'] == [{
        'data': {
            'username': 'rodrigo',
            'id': 1
        },
        'hand': [],
        'score': 0,
        'is_ready': False
    }, {
        'data': {
            'username': 'steve',
            'id': 2
        },
        'hand': [],
        'score': 0,
        'is_ready': False
    }]


def test_distribute_cards(test_client, init_game_db):
    room = Room.query.first()

    room.distribute_cards(7)

    game_data = room.load_game()

    assert len(game_data['players'][0]['hand']) == 7
    assert len(game_data['players'][1]['hand']) == 7
    assert len(game_data['discarded_cards']) == 14
    assert game_data['state'] == 'Selecting'


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
    czar_id = game_data['czar_id']
    selector_index = 0
    voter_index = 1

    if czar_id == 1:
        selector_index = 1
        voter_index = 0
        room.set_cards_for_user(2, [game_data['players'][1]['hand'][0]])

    else:
        selector_index = 0
        voter_index = 1
        room.set_cards_for_user(1, [game_data['players'][0]['hand'][0]])

    game_data = room.load_game()

    assert len(game_data['players'][selector_index]['hand']) == 6
    assert len(game_data['players'][voter_index]['hand']) == 7
    assert game_data['selected_cards'][0]['user']['id'] == game_data['players'][selector_index]['data']['id']
    assert len(game_data['selected_cards'][0]['cards']) == 1
    assert type(game_data['selected_cards'][0]['cards'][0]) is dict
    assert game_data['players'][selector_index]['is_ready'] == True
    assert game_data['players'][voter_index]['is_ready'] == False

    assert game_data['all_players_ready'] == True
    assert game_data['state'] == 'Voting'


def test_pick_winner(test_client, init_game_db):
    room = Room.query.first()

    game_data = room.load_game()

    winner_id = game_data['players'][0]['data']['id']

    room.pick_winner(winner_id)

    game_data = room.load_game()

    assert game_data['round_winner']['id'] == winner_id
    assert game_data['players'][0]['score'] == 1
    assert game_data['state'] == 'Results'


def test_start_new_round(test_client, init_game_db):
    room = Room.query.first()

    room.start_new_round()

    game_data = room.load_game()

    assert type(game_data['table_card']) is dict
    assert type(game_data['czar_id']) is int
    assert game_data['round_winner'] is None
    assert len(game_data['players'][0]['hand']) == 7
    assert len(game_data['players'][1]['hand']) == 7
    assert game_data['selected_cards'] == []
    assert game_data['players'][0]['is_ready'] == False
    assert game_data['players'][1]['is_ready'] == False
    assert game_data['all_players_ready'] == False
    assert game_data['state'] == 'Selecting'


def test_remove_user(test_client, init_game_db):
    room = Room.query.first()

    room.remove_user(2)

    game_data = room.load_game()

    assert len(game_data['players']) == 1
