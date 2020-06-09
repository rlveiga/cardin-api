from time import sleep

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
    print('game has started')
    room_code = data['room']

    current_room = Room.query.filter_by(code=room_code).first()

    if len(current_room.users) < 3:
        emit('start_response', {
             'error': 'Mínimo de 3 jogadores na sala para iniciar a partida'})

    else:
        max_ponts = data['max_points']

        current_room.create_new_game(max_ponts)
        current_room.start_game()

        game = current_room.load_game()

        emit('start_response', game.load_game_data(), room=room_code)

        game_data = game.load_game_data()
        current_round = game_data['round_number']

        sleep(60)

        handle_inactive_players(data, current_round)


def handle_inactive_players(data, current_round):
    print('handling inactive players')
    room_code = data['room']

    current_room = Room.query.filter_by(code=room_code).first()
    game = current_room.load_game()
    game_data = game.load_game_data()

    if game_data['state'] == 'Selecting' and current_round == game_data['round_number']:
        for player in game_data['players']:
            if game_data['czar_id'] != player['data']['id']:
                timed_out = True

                for selected_cards in game_data['selected_cards']:
                    if selected_cards['user']['id'] == player['data']['id']:
                        timed_out = False
                        break

                if timed_out:
                    print('user timed out')
                    data['user_id'] = player['data']['id']
                    data['cards'] = []

                    cards_selected(data)


@socketio.on('cards_selected')
def cards_selected(data):
    room_code = data['room']

    current_room = Room.query.filter_by(code=room_code).first()
    game = current_room.load_game()

    game.set_cards_for_user(data['user_id'], data['cards'])

    emit('cards_selected_response', game.load_game_data(), room=room_code)

    game_data = game.load_game_data()

    # Last player has selected cards, check to see
    # if any players have played at all
    if game_data['state'] == 'Voting':
        if len(game_data['selected_cards']) == 0:
            sleep(5)
            pick_winner(data)


@socketio.on('pick_winner')
def pick_winner(data):
    print('winner picked')
    room_code = data['room']
    winner_id = data.get('winner_id')

     current_room = Room.query.filter_by(code=room_code).first()
      game = current_room.load_game()

       if winner_id is not None:
            game.pick_winner(winner_id)

            emit('pick_winner_response', game.load_game_data(), room=room_code)

        sleep(5)

        new_round_start(data)


def new_round_start(data):
    print('new round started')
    room_code = data['room']

    current_room = Room.query.filter_by(code=room_code).first()
    game = current_room.load_game()

    game.start_new_round()

    emit('new_round_start_response', game.load_game_data(), room=room_code)

    game_data = game.load_game_data()
    current_round = game_data['round_number']

    sleep(60)

    handle_inactive_players(data, current_round)


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
