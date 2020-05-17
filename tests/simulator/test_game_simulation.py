import random

from time import sleep
from app.models.collection import Collection
from app.models.room import Room
from app.models.schemas import collection_share_schema
from app.models.user import User


def test_game_simulator(test_client, init_game_simulator_db, token):
    max_points = 15
    num_players = 10

    room = Room.query.first()

    for i in range(2, num_players + 1):
        room.add_user(i)

    collection = Collection.query.filter_by(id=room.collection_id).first()

    room.create_new_game(max_points)
    game = room.load_game()

    game.start_game(collection.id)

    game_data = game.load_game_data()

    while game_data['state'] != 'End':
        for player in game_data['players']:
            if player['data']['id'] != game_data['czar_id']:
                selected_cards = []
                slots = game_data['table_card']['slots']

                for i in range(slots):
                    random_card = player['hand'].pop(
                        (random.randrange(len(player['hand']))))
                    selected_cards.append(random_card)

                game.set_cards_for_user(player['data']['id'], selected_cards)

        game_data = game.load_game_data()
        winner_id = 0

        while(winner_id == 0):
            random_winner = game_data['players'][random.randrange(
                len(game_data['players']))]

            if random_winner['data']['id'] != game_data['czar_id']:
                winner_id = random_winner['data']['id']

        game.pick_winner(winner_id)
        game.start_new_round()
        game_data = game.load_game_data()

        print('Scores:')
        for player in game_data['players']:
          print(f"Player {player['data']['id']}: {player['score']}")
          print(f"Hand length: {len(player['hand'])}")

        print(f"Remaining white cards: {len(game_data['white_cards'])}")
        print(f"Remaining black cards: {len(game_data['black_cards'])}")

        sleep(1)