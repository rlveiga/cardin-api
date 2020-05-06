from app.models.room import Room
from app.models.user import User
from app.models.collection import Collection
from app.models.schemas import collection_share_schema

import random


def test_init_game_data(test_client, init_game_db, token):
    room = Room.query.first()
    collection = Collection.query.filter_by(id=room.collection_id).first()

    room.create_new_game(15)
    game = room.load_game()

    game.init_game_data(collection)
    game_data = game.load_game_data()

    assert game_data['state'] == 'Zero'
    assert game_data['collection'] == collection_share_schema.dump(collection)
    assert len(game_data['all_cards']) == 0
    assert len(game_data['white_cards']) == 0
    assert len(game_data['black_cards']) == 0
    assert game_data['discarded_cards'] == []
    assert game_data['table_card'] is None
    assert game_data['players'] == [{
        'data': {
            'id': 1,
            'name': 'user_1',
            'username': None,
            'profile_img': None,
            'source': 'cardin',
            'profile_color': '#000000'
        },
        'hand': [],
        'score': 0,
        'is_ready': False
    }, {
        'data': {
            'id': 2,
            'name': 'user_2',
            'username': None,
            'profile_img': None,
            'source': 'cardin',
            'profile_color': '#000000'
        },
        'hand': [],
        'score': 0,
        'is_ready': False
    }, {
        'data': {
            'id': 3,
            'name': 'user_3',
            'username': None,
            'profile_img': None,
            'source': 'cardin',
            'profile_color': '#000000'
        },
        'hand': [],
        'score': 0,
        'is_ready': False
    }]
    assert game_data['selected_cards'] == []
    assert game_data['czar_id'] is None
    assert game_data['round_winner'] is None
    assert game_data['all_players_ready'] == False
    assert game_data['game_winner'] is None

    assert room.status == 'active'

def test_create_deck(test_client, init_game_db, token):
    room = Room.query.first()
    collection = Collection.query.filter_by(id=room.collection_id).first()
    game = room.load_game()

    game.create_deck(collection.cards)
    game_data = game.load_game_data()

    assert len(game_data['all_cards']) > 0
    assert len(game_data['white_cards']) > 0
    assert len(game_data['black_cards']) > 0


def test_distribute_cards(test_client, init_game_db):
    room = Room.query.first()
    game = room.load_game()

    game.distribute_cards()

    game_data = game.load_game_data()

    assert len(game_data['players'][0]['hand']) == 7
    assert len(game_data['players'][1]['hand']) == 7
    assert len(game_data['players'][2]['hand']) == 7
    assert len(game_data['discarded_cards']) == 21


def test_pick_table_card(test_client, init_game_db):
    room = Room.query.first()
    game = room.load_game()

    game.pick_table_card()

    game_data = game.load_game_data()

    assert game_data['table_card'] is not None
    assert len(game_data['discarded_cards']) == 22


def test_pick_czar(test_client, init_game_db):
    room = Room.query.first()
    game = room.load_game()

    game.pick_czar()

    game_data = game.load_game_data()

    assert type(game_data['czar_id']) is int
    assert game_data['state'] == 'Selecting'


def test_set_cards_for_user(test_client, init_game_db):
    room = Room.query.first()
    game = room.load_game()

    game_data = game.load_game_data()
    czar_id = game_data['czar_id']

    for player in game_data['players']:
      player_id = player['data']['id']

      if player_id != czar_id:
        cards = []

        for i in range(game_data['table_card']['slots']):
          cards.append(player['hand'][i])

        game.set_cards_for_user(player_id, cards)

    game_data = game.load_game_data()

    for player in game_data['players']:
      player_id = player['data']['id']

      if player_id == czar_id:
        assert len(player['hand']) == 7

      else:
        assert len(player['hand']) < 7

    assert len(game_data['selected_cards']) == 2
    assert type(game_data['selected_cards'][0]['cards'][0]) is dict
    assert game_data['all_players_ready'] == True
    assert game_data['state'] == 'Voting'


def test_pick_winner(test_client, init_game_db):
    room = Room.query.first()
    game = room.load_game()

    game_data = game.load_game_data()
    
    for (i, player) in enumerate(game_data['players']):
      # Choose first player as winner
      if player['data']['id'] != game_data['czar_id']:
        winner_id = player['data']['id']

    game.pick_winner(winner_id)

    game_data = game.load_game_data()

    assert game_data['round_winner']['id'] == winner_id
    assert game_data['players'][winner_id - 1]['score'] == 1
    assert game_data['state'] == 'Results'


def test_start_new_round(test_client, init_game_db):
    room = Room.query.first()
    game = room.load_game()

    game.start_new_round()

    game_data = game.load_game_data()

    assert type(game_data['table_card']) is dict
    assert type(game_data['czar_id']) is int
    assert game_data['round_winner'] is None
    assert len(game_data['players'][0]['hand']) == 7
    assert len(game_data['players'][1]['hand']) == 7
    assert len(game_data['players'][2]['hand']) == 7
    assert game_data['selected_cards'] == []
    assert game_data['players'][0]['is_ready'] == False
    assert game_data['players'][1]['is_ready'] == False
    assert game_data['players'][2]['is_ready'] == False
    assert game_data['all_players_ready'] == False
    assert game_data['state'] == 'Selecting'

def test_end_game(test_client, init_game_db):
    room = Room.query.first()
    game = room.load_game()

    game.end_game()

    assert room.status == 'inactive'
    assert game.discarded_at is not None

    game_data = game.load_game_data()

    assert type(game_data['game_winner']) is dict
    assert game_data['state'] == 'End'

# def test_remove_user(test_client, init_game_db):
#     room = Room.query.first()

#     room.remove_user(2)

#     game_data = game.load_game_data()

#     assert len(game_data['players']) == 1
