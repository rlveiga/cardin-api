import pytest
from app import create_app, db
from app.models.user import User
from app.models.room import Room, Association
from app.models.card import Card

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
    user = User(name='rodrigo', email='rlveiga@gmail.com')
    user.password = 'abc123'

    user2 = User(name='steve', email='steve@apple.com')
    user2.password = 'abc123'

    db.session.add(user)
    db.session.add(user2)
    db.session.commit()

    room1 = Room(code='test1', created_by=user.id)
    room2 = Room(code='test2', created_by=user2.id)

    db.session.add(room1)
    db.session.add(room2)
    db.session.commit()

    join = Association(user_id=1, room_id=1)
    join2 = Association(user_id=2, room_id=2)

    db.session.add(join)
    db.session.add(join2)
    db.session.commit()

    card1 = Card(card_type='black', card_text='I am starting to feel a')
    card2 = Card(card_type='white', card_text='Social justice')

    db.session.add(card1)
    db.session.add(card2)
    db.session.commit()

    yield db # actual testing

    db.session.close()
    db.drop_all()

@pytest.fixture(scope='module')
def token():
    user = User.query.filter_by(id=1).first()
    token = user.generate_auth_token(3600).decode('UTF-8')

    yield token