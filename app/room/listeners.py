from app import socketio
from app.models.room import Room
from app.models.schemas import users_share_schema

from flask_socketio import emit, join_room, leave_room, rooms


@socketio.on('join')
def join(data):
    room_code = data['room']
    user = data['user']

    current_room = Room.query.filter_by(code=room_code).first()

    join_room(room_code)

    emit('join_response', {'users': users_share_schema.dump(
        current_room.users)}, room=room_code)


@socketio.on('leave')
def leave(data):
    room_code = data['room']
    user = data['user']

    current_room = Room.query.filter_by(code=room_code).first()
    game = current_room.load_game()
    game_data = None

    if game is not None:
        game_data = game.load_game_data()

    leave_room(room_code)

    emit('leave_response', {'users': users_share_schema.dump(
        current_room.users), 'game': game_data}, room=room_code)


@socketio.on('game_start')
def game_start(data):
    room_code = data['room']

    current_room = Room.query.filter_by(code=room_code).first()

    if len(current_room.users) < 3:
        emit('start_response', {
             'error': 'Mínimo de 3 jogadores na sala para iniciar a partida'})

    else:
        current_room.create_new_game(3)
        current_room.start_new_game()

        game = current_room.load_game()

        emit('start_response', game.load_game_data(), room=room_code)


@socketio.on('cards_selected')
def cards_selected(data):
    room_code = data['room']

    current_room = Room.query.filter_by(code=room_code).first()
    game = current_room.load_game()

    game.set_cards_for_user(data['user_id'], data['cards'])

    emit('cards_selected_response', game.load_game_data(), room=room_code)


@socketio.on('pick_winner')
def pick_winner(data):
    room_code = data['room']
    winner_id = data['winner_id']

    current_room = Room.query.filter_by(code=room_code).first()
    game = current_room.load_game()

    game.pick_winner(winner_id)

    emit('pick_winner_response', game.load_game_data(), room=room_code)


@socketio.on('new_round_start')
def new_round_start(data):
    room_code = data['room']

    current_room = Room.query.filter_by(code=room_code).first()
    game = current_room.load_game()

    game.start_new_round()

    emit('new_round_start_response', game.load_game_data(), room=room_code)


@socketio.on('card_swipe')
def card_swipe(data):
    print(data)
    room_code = data['room']

    emit('card_swipe_response', data['index'], room=room_code)


@socketio.on('discard_option')
def discard_option(data):
    print('discard', data)
    room_code = data['room']

    current_room = Room.query.filter_by(code=room_code).first()
    game = current_room.load_game()

    game.discard_option(data['user_id'])

    emit('discard_option_response', game.load_game_data(), room=room_code)
