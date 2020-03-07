import json

from app.models.room import Room, RoomAssociation

def test_game_start(test_client, init_db, init_room_db, token):
  response = test_client.put('/rooms/start_game?room=test2', headers={'access-token': token})

  data = json.loads(response.data)

  assert response.status_code == 201

  # Room must have at least three members
  assert data['room']['game_data']['state'] == 'Zero'
  # assert len(data['users']) >= 3
  assert data['room']['game_data'] is not None
  assert type(data['room']['game_data']['deck']) is list
  # assert type(data['room']['data']['all_cards']) is list
  # assert type(data['room']['data']['white_cards']) is list
  # assert type(data['room']['data']['black_cards']) is list
  assert data['room']['game_data']['scores'] == [0] * len(data['users'])

def test_game_end(test_client, init_db, init_room_db, token):
  response = test_client.put('/rooms/end_game?room=test2', headers={'access-token': token})

  data = json.loads(response.data)

  assert response.status_code == 201
  
  assert len(data.users) == 0
  assert data.status == 'inactive'
  assert data.game_data is None