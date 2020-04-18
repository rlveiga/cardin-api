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

# Creates db and test users
@pytest.fixture
def init_db():
    # Create the test db
    db.create_all()

    # Populate with data

    # Create test users
    user1 = User(username='rodrigo')
    user1.password = 'abc123'

    user2 = User(username='steve')
    user2.password = 'abc123'

    users = [
        user1,
        user2
    ]

    db.session.add_all(users)
    db.session.commit()

    room1 = Room(code='test1', created_by=user1.id)

    db.session.add(room1)
    db.session.commit()

    yield db  # actual testing

    db.session.close()
    db.drop_all()


@pytest.fixture
def init_cards_collections_db():
    # Default collections
    default_collection1 = Collection(
        name="Minhas cartas", created_by=1, editable=False)
    default_collection2 = Collection(
        name="Minhas cartas", created_by=2, editable=False)

    # User 1's collections
    collection1 = Collection(name='Test collection', created_by=1)
    collection2 = Collection(name="Deletable collection", created_by=1)

    # User 2's collections
    collection3 = Collection(name="Steve's collection", created_by=2)

    collections = [
        default_collection1,
        default_collection2,
        collection1,
        collection2,
        collection3
    ]

    db.session.add_all(collections)
    db.session.commit()

    # Collection ownerships
    ownership1 = OwnedCollection(
        collection_id=default_collection1.id, user_id=1)
    ownership2 = OwnedCollection(
        collection_id=default_collection2.id, user_id=2)
    ownership3 = OwnedCollection(collection_id=collection1.id, user_id=1)
    ownership4 = OwnedCollection(collection_id=collection2.id, user_id=1)
    ownership5 = OwnedCollection(collection_id=collection3.id, user_id=2)

    ownerships = [
        ownership1,
        ownership2,
        ownership3,
        ownership4,
        ownership5
    ]

    db.session.add_all(ownerships)
    db.session.commit()

    # Test cards
    # User 1's cards
    card1 = Card(card_type='black', name='I am starting to feel', created_by=1)
    card2 = Card(card_type='white', name='Deletable card', created_by=1)

    # User 2's cards
    card3 = Card(card_type='white', name='Social justice', created_by=2)
    card4 = Card(card_type='white', name='Undeletable card', created_by=2)

    cards = [
        card1,
        card2,
        card3,
        card4
    ]

    db.session.add_all(cards)
    db.session.commit()

    # Test card associations
    # User 1's card associations
    card_association1 = CardAssociation(
        card_id=card1.id, collection_id=collection1.id)
    card_association2 = CardAssociation(
        card_id=card2.id, collection_id=collection1.id)

    # User 2's card associations
    card_association3 = CardAssociation(
        card_id=card3.id, collection_id=collection3.id)

    card_associations = [
        card_association1,
        card_association2,
        card_association3
    ]

    db.session.add_all(card_associations)
    db.session.commit()

    yield db

    db.session.close()
    db.drop_all()

# Creates rooms and associations for testing
@pytest.fixture
def init_room_db():

    # Test rooms, room1 created in conftest.py
    room2 = Room(code='test2', created_by=1)
    room3 = Room(code='test3', created_by=2)

    rooms = [
        room2,
        room3
    ]

    db.session.add_all(rooms)
    db.session.commit()

    # Test room associations
    # User 1 room association
    room_association1 = RoomAssociation(user_id=1, room_id=2)

    # User 2 room associations
    room_association2 = RoomAssociation(user_id=2, room_id=3)

    room_associations = [
        room_association1,
        room_association2
    ]

    db.session.add_all(room_associations)
    db.session.commit()

    yield db  # actual testing

    db.session.close()
    db.drop_all()


@pytest.fixture
def token():
    # Testing as user with id = 1
    user = User.query.filter_by(id=1).first()
    token = user.generate_auth_token(3600).decode('UTF-8')

    yield token


@pytest.fixture(scope='module')
def init_game_db(test_client):
    db.create_all()

    # Create test users
    user1 = User(username='rodrigo')
    user1.password = 'abc123'

    user2 = User(username='steve')
    user2.password = 'abc123'

    users = [
        user1,
        user2
    ]

    db.session.add_all(users)
    db.session.commit()

    room1 = Room(code='test1', created_by=user1.id)

    db.session.add(room1)
    db.session.commit()

    collection = Collection(name='Test collection')

    db.session.add(collection)
    db.session.commit()
    
    collection.create_from_file('decks/default_1', 'csv')

    yield db

    db.session.close()
    db.drop_all()
