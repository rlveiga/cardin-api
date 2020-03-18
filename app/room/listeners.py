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
    current_room.init_game()

    emit('start_response', current_room.load_game(), room=room_code)


@socketio.on('cards_selected')
def cards_selected(data):
    room_code = data['room']

    current_room = Room.query.filter_by(code=room_code).first()

    current_room.set_cards_for_user(data['user_id'], data['cards'])

    # Notify players in room that user with
    # data['user_id'] has played his cards
    emit('cards_selected_response', data['user_id'], room=room_code)

@socketio.on('pick_winner')
def pick_winner(data)
    room_code = data['room']
    winner_id = data['winner_id']

    current_room = Room.query.filter_by(code=room_code).first()

    current_room.pick_winner(winner_id)

    emit('pick_winner_response', current_room.load_game(), room=room_code)

@socketio.on('new_round_start')
def new_round_start(data)
    room_code = data['room']
    
    current_room = Room.query.filter_by(code=room_code).first()

    current_room.start_new_round()

    emit('new_round_start_response', game.load_game(), room=room_code)