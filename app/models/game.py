import json
import random
from datetime import datetime

from app import db
from app.models.schemas import (card_share_schema, cards_share_schema,
                                collection_share_schema,
                                user_share_schema)
from app.models.user import User
from app.models.collection import Collection


class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    max_points = db.Column(db.Integer, nullable=False)
    game_data = db.Column(db.String(500000))
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow(), nullable=False)
    discarded_at = db.Column(db.DateTime)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)

    def add_new_player(self, user_id):
        game_data = self.load_game_data()

        user_dict = user_share_schema.dump(
            User.query.filter_by(id=user_id).first())

        game_data['players'].append({
            'data': user_dict,
            'hand': [],
            'score': 0,
            'is_ready': False
        })

        self.game_data = json.dumps(game_data)

    def remove_player(self, user_id):
        game_data = self.load_game_data()

        for player in game_data['players']:
            if player['data']['id'] == user_id:
                game_data['players'].remove(player)

        if len(game_data['players']) < 3:
            print('game ended')
            self.end_game()

    def start_game(self, collection_id):
        collection = Collection.query.filter_by(id=collection_id).first()

        self.init_game_data(collection)
        self.create_deck(collection.cards)
        self.distribute_cards()
        self.pick_table_card()
        self.pick_czar()

        db.session.commit()

    # Game state is stored as metadata
    def init_game_data(self, collection):
        game_data = {
            'state': 'Zero',
            'collection': collection_share_schema.dump(collection),
            'all_cards': [],
            'white_cards': [],
            'black_cards': [],
            'discarded_cards': [],
            'table_card': None,
            'players': [],
            'selected_cards': [],
            'czar_id': None,
            'round_winner': None,
            'all_players_ready': False,
            'game_winner': None,
            'max_points': self.max_points
        }

        users_in_room = self.room.users

        for user in users_in_room:
            user_dict = user_share_schema.dump(user)
            game_data['players'].append({
                'data': user_dict,
                'hand': [],
                'score': 0,
                'is_ready': False
            })

        self.room.status = 'active'
        self.game_data = json.dumps(game_data)

    def create_deck(self, cards):
        game_data = self.load_game_data()
        game_data['all_cards'] = cards_share_schema.dump(cards)

        for card in cards:
            if(card.card_type == 'black'):
                game_data['black_cards'].append(card_share_schema.dump(card))

            elif(card.card_type == 'white'):
                game_data['white_cards'].append(card_share_schema.dump(card))

        self.game_data = json.dumps(game_data)

    def start_new_round(self):
        leaderboard = self.get_leaderboard()
        highest_score = leaderboard[0]['score']

        if highest_score == self.max_points:
            self.end_game()

        else:
            self.distribute_cards()
            self.pick_table_card()
            self.pick_czar()

            game_data = self.load_game_data()

            game_data['round_winner'] = None
            game_data['selected_cards'] = []

            for player in game_data['players']:
                player['is_ready'] = False

            game_data['all_players_ready'] = False

            self.game_data = json.dumps(game_data)

    # Randomly assigns white cards to hands,
    # until hand length == 7
    def distribute_cards(self):
        game_data = self.load_game_data()
        white_card_list = game_data['white_cards']

        for player in game_data['players']:
            while len(player['hand']) != 7:
                selected_card = white_card_list.pop(
                    random.randrange(len(white_card_list)))

                game_data['discarded_cards'].append(selected_card)
                player['hand'].append(selected_card)

        self.game_data = json.dumps(game_data)

    # Randomly select a card prom black cards to
    # be played, to be called upon game start and
    # round end
    def pick_table_card(self):
        game_data = self.load_game_data()
        black_card_list = game_data['black_cards']

        selected_card = black_card_list.pop(
            random.randrange(len(black_card_list)))
        game_data['table_card'] = selected_card
        game_data['discarded_cards'].append(selected_card)

        self.game_data = json.dumps(game_data)

    def pick_czar(self):
        game_data = self.load_game_data()
        new_czar_id = self.room.users[random.randrange(
            len(self.room.users))].id

        game_data['czar_id'] = new_czar_id
        game_data['state'] = 'Selecting'

        self.game_data = json.dumps(game_data)

    def set_cards_for_user(self, user_id, user_cards):
        game_data = self.load_game_data()

        user = User.query.filter_by(id=user_id).first()

        # Indicates that the player has not timed out and cards where chosen
        if user_cards != []:
            cards = []

            table_slots = game_data['table_card']['slots']

            if table_slots == 0 or table_slots == 1:
                if len(user_cards) != 1:
                    print(
                        f"{len(user_cards)} cartas enviadas, {table_slots} necessárias")
                    return

            else:
                if len(user_cards) != table_slots:
                    print(
                        f"{len(user_cards)} cartas enviadas, {table_slots} necessárias")
                    return

            for card in user_cards:
                cards.append(card_share_schema.dump(card))

            selected_cards = {
                'user': user_share_schema.dump(user),
                'cards': cards,
                'discarded': False
            }

            game_data['selected_cards'].append(selected_cards)

            for player in game_data['players']:
                if player['data']['id'] == user_id:
                    for selected_card in user_cards:
                        print('selected: ', selected_card)
                        print('hand: ', player['hand'])
                        player['hand'].remove(selected_card)
                    player['is_ready'] = True

        else:
            for player in game_data['players']:
                if player['data']['id'] == user_id:
                    player['is_ready'] = True

        all_players_ready = True
        state = 'Voting'

        for player in game_data['players']:
            if player['is_ready'] == False and game_data['czar_id'] != player['data']['id']:
                state = 'Selecting'
                all_players_ready = False

        game_data['all_players_ready'] = all_players_ready
        game_data['state'] = state

        self.game_data = json.dumps(game_data)

    def pick_winner(self, winner_id):
        game_data = self.load_game_data()

        for player in game_data['players']:
            if player['data']['id'] == winner_id:
                game_data['round_winner'] = player['data']
                player['score'] += 1

        game_data['state'] = 'Results'

        self.game_data = json.dumps(game_data)

    def discard_option(self, user_id):
        game_data = self.load_game_data()

        for option in game_data['selected_cards']:
            if option['user']['id'] == user_id:
                option['discarded'] = True

        self.game_data = json.dumps(game_data)

    def load_game_data(self):
        if self.game_data is not None:
            game_data = json.loads(self.game_data)

            return game_data

        return self.game_data

    def end_game(self):
        game_data = self.load_game_data()

        sorted_list = self.get_leaderboard()

        game_data['game_winner'] = sorted_list[0]['data']
        game_data['state'] = 'End'

        self.discarded_at = datetime.now()
        self.game_data = json.dumps(game_data)
        self.room.status = 'inactive'

        db.session.commit()

    def get_leaderboard(self):
        game_data = self.load_game_data()

        return sorted(game_data['players'], key=lambda k: k['score'], reverse=True)
