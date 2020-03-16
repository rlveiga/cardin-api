from app import socketio
from flask_socketio import emit, join_room, leave_room, rooms

@socketio.on('join')
def join(data):
    room_code = data['room']
    user = data['user']

    join_room(room_code)

    emit('join_response', {'user': user}, room=room_code)

@socketio.on('leave')
def leave(data):
    room_code = data['room']
    user = data['user']

    leave_room(room_code)

    emit('leave_response', {'user': user}, room=room_code)