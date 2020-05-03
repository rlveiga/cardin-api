import json

from app.models.room import Room, RoomAssociation
from app.models.collection import Collection
from app.models.schemas import collection_share_schema


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

# def test_get_user_room(test_client, init_db, token):
#     response = test_client.get('/rooms/', headers={'access-token': token})

#     data = json.loads(response.data)

#     assert response.status_code == 200

#     assert type(data['room']) is dict
#     assert data['room']['code'] == 'test1'


# def test_distribute_cards(test_client, init_db):
#     room = Room.query.filter_by(code='test1').first()

#     room.distribute_cards(7)

#     game_data = room.load_game()

#     assert len(game_data['players'][0]['hand']) == 7
#     assert len(game_data['players'][1]['hand']) == 7
#     assert len(game_data['discarded_cards']) == 14
#     assert game_data['state'] == 'Selecting'


# def test_pick_table_card(test_client, init_db):
#     room = Room.query.filter_by(code='test1').first()

#     room.pick_table_card()

#     game_data = room.load_game()

#     assert game_data['table_card'] is not None
#     assert len(game_data['discarded_cards']) == 15


# def test_pick_czar(test_client, init_db):
#     room = Room.query.filter_by(code='test1').first()

#     room.pick_czar()

#     game_data = room.load_game()

#     assert type(game_data['czar_id']) is int


# # TODO - THIS TEST CURRENTLY DEPENDS ON RANDOM VALUES TO WORK
# def test_set_cards_for_user(test_client, init_db):
#     room = Room.query.filter_by(code='test1').first()

#     game_data = room.load_game()
#     czar_id = game_data['czar_id']
#     selector_index = 0
#     voter_index = 1

#     if czar_id == 1:
#         selector_index = 0
#         voter_index = 1
#         cards_used = 1

#         cards = []

#         if game_data['table_card']['slots'] == 0 or game_data['table_card']['slots'] == 1:
#             cards = [game_data['players'][0]['hand'][0]]

#         else:
#             cards = [game_data['players'][0]['hand']
#                      [0], game_data['players'][0]['hand'][1]]
#             cards_used = 2

#         room.set_cards_for_user(2, cards)

#     else:
#         selector_index = 1
#         voter_index = 0
#         cards_used = 1

#         cards = []

#         if game_data['table_card']['slots'] == 0 or game_data['table_card']['slots'] == 1:
#             cards = [game_data['players'][1]['hand'][0]]

#         else:
#             cards = [game_data['players'][1]['hand']
#                      [0], game_data['players'][1]['hand'][1]]
#             cards_used = 2

#         room.set_cards_for_user(1, cards)

#     game_data = room.load_game()

#     assert len(game_data['players'][selector_index]['hand']) == 7 - cards_used
#     assert len(game_data['players'][voter_index]['hand']) == 7
#     assert game_data['selected_cards'][0]['user']['id'] == game_data['players'][selector_index]['data']['id']
#     assert len(game_data['selected_cards'][0]['cards']) == 1
#     assert type(game_data['selected_cards'][0]['cards'][0]) is dict
#     assert game_data['players'][selector_index]['is_ready'] == True
#     assert game_data['players'][voter_index]['is_ready'] == False

#     assert game_data['all_players_ready'] == True
#     assert game_data['state'] == 'Voting'


# def test_pick_winner(test_client, init_db):
#     room = Room.query.filter_by(code='test1').first()

#     game_data = room.load_game()

#     winner_id = game_data['players'][0]['data']['id']

#     room.pick_winner(winner_id)

#     game_data = room.load_game()

#     assert game_data['round_winner']['id'] == winner_id
#     assert game_data['players'][0]['score'] == 1
#     assert game_data['state'] == 'Results'


# # TODO - THIS TEST CURRENTLY DEPENDS ON RANDOM VALUES TO WORK
# def test_start_new_round(test_client, init_db):
#     room = Room.query.filter_by(code='test1').first()

#     room.start_new_round()

#     game_data = room.load_game()

#     assert type(game_data['table_card']) is dict
#     assert type(game_data['czar_id']) is int
#     assert game_data['round_winner'] is None
#     assert len(game_data['players'][0]['hand']) == 7
#     assert len(game_data['players'][1]['hand']) == 7
#     assert game_data['selected_cards'] == []
#     assert game_data['players'][0]['is_ready'] == False
#     assert game_data['players'][1]['is_ready'] == False
#     assert game_data['all_players_ready'] == False
#     assert game_data['state'] == 'Selecting'


# # def test_get_room_players(test_client, init_db, init_room_db, token):
# #     pass

# # def test_get_unexisting_room_players(test_client, init_db, token):
# #     response = test_client.get('/rooms/four2', headers={'access-token': token})

# #     data = json.loads(response.data)

# #     assert response.status_code == 404

# #     assert data['message'] == 'Room not found'

# # def test_create_room(test_client, init_db, init_cards_collections_db, token):
# #     response = test_client.post('/rooms/', json=dict(code='abcde', collection_id=1), headers={'access-token': token})

# #     data = json.loads(response.data)

# #     assert response.status_code == 200
# #     assert type(data['data']) is dict
# #     assert type(data['users']) is list
# #     assert type(data['game']) is dict

# # def test_leave_room_as_host(test_client, init_db, init_room_db, token):
# #     response = test_client.delete('/rooms/test2', headers={'access-token': token})

# #     data = json.loads(response.data)

# #     assert response.status_code == 200
# #     assert data['room']['status'] == 'inactive'


# # def test_search_room(test_client, init_db, init_room_db, token):
# #     response = test_client.get('/rooms/test1', headers={'access-token': token})

# #     data = json.loads(response.data)

# #     assert response.status_code == 200

# #     assert data['room']['data']['code'] == 'test1'

# # def test_search_unexisting_room(test_client, init_db, token):
# #     response = test_client.get('/rooms/random', headers={'access-token': token})

# #     data = json.loads(response.data)

# #     assert response.status_code == 404

# #     assert data['message'] == 'Room not found'
