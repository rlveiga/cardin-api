import json

from app.models.room import Room, RoomAssociation

def test_game_start(test_client, init_db, init_room_db, init_cards_collections_db, token):
  response = test_client.put('/rooms/start_game/2', json=dict(collection_id=1), headers={'access-token': token})

  data = json.loads(response.data)

  assert response.status_code == 201

  # Room must have at least three members
  assert data['room']['game_data']['state'] == 'Zero'
  # assert len(data['users']) >= 3
  assert data['room']['game_data'] is not None
  assert type(data['room']['game_data']['all_cards']) is list
  assert len(data['room']['game_data']['all_cards']) >= 0
  assert type(data['room']['game_data']['white_cards']) is list
  assert len(data['room']['game_data']['white_cards']) >= 0
  assert type(data['room']['game_data']['black_cards']) is list
  assert len(data['room']['game_data']['black_cards']) >= 0
  assert data['room']['game_data']['scores'] == [0] * len(data['users'])

def test_game_end(test_client, init_db, init_room_db, token):
  response = test_client.put('/rooms/end_game?room=test2', headers={'access-token': token})

  data = json.loads(response.data)

  assert response.status_code == 201
  
  assert len(data.users) == 0
  assert data.status == 'inactive'
  assert data.game_data is None