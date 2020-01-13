import pytest
from app import create_app, db
from app.models.user import User
from app.models.room import Room, Association
from app.models.card import Card
from app.models.collection import Collection

@pytest.fixture(scope='module')
def test_client():
    # Flask provides a way to test the application by exposing the Werkzeug test Client
    # and handling the context locals.
    flask_app = create_app('testing')
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client # actual testing

    ctx.pop()

@pytest.fixture(scope='module')
def init_db():
    # Create the test db
    db.create_all()

    # Populate with data
    user1 = User(username='rodrigo')
    user1.password = 'abc123'

    user2 = User(username='steve')
    user2.password = 'abc123'

    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    collection1 = Collection(name='Test collection', created_by=user1.id)
    collection2 = Collection(name="Steve's collection", created_by=user2.id)
    collection3 = Collection(name='Deletable collection', created_by=user1.id)

    db.session.add(collection1)
    db.session.add(collection2)
    db.session.add(collection3)
    db.session.commit()

    card1 = Card(card_type='black', name='I am starting to feel', collection_id=collection1.id, created_by=user1.id)
    card2 = Card(card_type='white', name='Social justice', collection_id=collection2.id, created_by=user2.id)
    card3 = Card(card_type='white', name='Deletable card', collection_id=collection1.id, created_by=user1.id)
    card4 = Card(card_type='white', name='Undeletable card', collection_id=collection2.id, created_by=user2.id)

    db.session.add(card1)
    db.session.add(card2)
    db.session.commit()

    room1 = Room(code='test1', created_by=user1.id)
    room2 = Room(code='test2', created_by=user2.id)

    db.session.add(room1)
    db.session.add(room2)
    db.session.commit()

    join1 = Association(user_id=1, room_id=1)
    join2 = Association(user_id=2, room_id=2)

    db.session.add(join1)
    db.session.add(join2)
    db.session.commit()    

    yield db # actual testing

    db.session.close()
    db.drop_all()

@pytest.fixture(scope='module')
def token():
    user = User.query.filter_by(id=1).first()
    token = user.generate_auth_token(3600).decode('UTF-8')

    yield token