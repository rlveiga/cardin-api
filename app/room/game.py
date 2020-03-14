from app import socketio
from flask_socketio import emit, join_room, leave_room, rooms

@socketio.on('join')
def join(data):
    print('join')
    room_code = data['room']
    user = data['user']

    join_room(room_code)

    emit('join_response', f"{user['username']} has joined {room_code}", room=room_code)

@socketio.on('leave')
def on_leave(data):
    room_code = data['room']
    user = data['user']

    leave_room(room_code)

    emit('leave_response', f"{user} has left {room_code}", room=room_code)