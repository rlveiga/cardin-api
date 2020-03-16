from app import socketio
from app.models.room import Room

from flask_socketio import emit, join_room, leave_room, rooms


@socketio.on('join')
def join(data):
    room_code = data['room']
    user = data['user']

    current_room = Room.query.filter_by(code=room_code).first()
    print(current_room.code)

    join_room(room_code)

    emit('join_response', user, room=room_code)


@socketio.on('leave')
def leave(data):
    room_code = data['room']
    user = data['user']

    leave_room(room_code)

    emit('leave_response', user, room=room_code)

@socketio.on('game_start')
def game_start(data):
  room_code = data['room']

  current_room = Room.query.filter_by(code=room_code).first()

  emit('start_response', current_room.load_game(), room=room_code)