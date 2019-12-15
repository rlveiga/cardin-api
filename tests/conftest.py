import pytest
from app import create_app, db
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

    yield testing_client # actual testing

    ctx.pop()

@pytest.fixture(scope='module')
def init_db():
    # Create the test db
    db.create_all()

    # Populate with data
    user1 = User(name='rodrigo', email='rlveiga@gmail.com')
    user1.password = 'abc123'
    
    db.session.add(user1)
    db.session.commit()

    yield db # actual testing

    db.session.close()
    db.drop_all()