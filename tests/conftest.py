import pytest

from app import create_app, db
from app.models.card import Card, CardAssociation
from app.models.collection import Collection, OwnedCollection
from app.models.room import Room, RoomAssociation
from app.models.user import User


@pytest.fixture(scope='module')
def test_client():
    # Flask provides a way to test the application by exposing the Werkzeug test Client
    # and handling the context locals.
    flask_app = create_app('testing')
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # actual testing

    ctx.pop()


@pytest.fixture(scope='module')
def init_db():
    # Create the test db
    db.create_all()

    # Create test users
    create_users(3)

    # Create one collection for our tester...
    create_collections(1, 1)

    # ... and one for secondary user
    create_collections(1, 2)

    # Fill collection with cards
    collection = Collection.query.filter_by(created_by=1).first()
    collection.create_from_file('decks/default_1', 'csv')

    # Create card for tester
    create_cards(1, 1)

    # and for secondary user
    create_cards(1, 2)

    # Create room for secondary user
    create_rooms(1, 2, 'waiting')

    # Create room with status active (game in progress)
    create_rooms(1, 3, 'active')

    yield db  # actual testing

    db.session.close()
    db.drop_all()


@pytest.fixture(scope='module')
def init_game_db():
    # Create the test db
    db.create_all()

    # Create test users
    create_users(3)

    # Create collection to be used in game
    create_collections(1, 1)

    # Fill collection with cards
    collection = Collection.query.filter_by(created_by=1).first()
    collection.create_from_file('decks/default_1', 'csv')

    # Create room to be used for game
    create_rooms(1, 1, 'waiting')

    # Add two more players to make game playable
    room = Room.query.filter_by(created_by=1).first()
    room.add_user(2)
    room.add_user(3)

    yield db  # actual testing

    db.session.close()
    db.drop_all()


def create_users(number_of_users):
    for i in range(number_of_users):
        user = User(username=f"user_{i+1}")

        db.session.add(user)
        db.session.commit()

        user.create_default_collection()


def create_collections(number_of_collections, creator_id):
    for i in range(number_of_collections):
        collection = Collection(
            name=f"collection_{i+1}", created_by=creator_id)

        db.session.add(collection)
        db.session.commit()


def create_cards(number_of_cards, creator_id):
    for i in range(number_of_cards):
        card = Card(name=f"card_{i+1}",
                    card_type='white', created_by=creator_id)

        db.session.add(card)
        db.session.commit()


def create_rooms(number_of_rooms, creator_id, room_status):
    for i in range(number_of_rooms):
        room = Room(
            code=f"room{len(Room.query.all()) + i + 1}", created_by=creator_id, status=room_status)

        db.session.add(room)
        db.session.commit()

        room.add_user(creator_id)


@pytest.fixture
def token():
    # Testing as user with id = 1
    user = User.query.filter_by(id=1).first()
    token = user.generate_auth_token(3600).decode('UTF-8')

    yield token
