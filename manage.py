import csv
import time

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

from app import app, db, socketio
from app.models.card import Card, CardAssociation
from app.models.collection import Collection, OwnedCollection
from app.models.room import Room, RoomAssociation
from app.models.game import Game
from app.models.user import User

manager = Manager(app)
Migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Card=Card, Collection=Collection, OwnedCollection=OwnedCollection, Room=Room, Game=Game, RoomAssociation=RoomAssociation)


@manager.command
def run():
    socketio.run(app)


@manager.command
def create_tables():
    db.create_all()


@manager.command
def create_collection(folder_path, collection_name, file_type):
    new_collection = Collection(name=collection_name, editable=False)
    db.session.add(new_collection)
    db.session.commit()

    new_collection.create_from_file(folder_path, file_type)


@manager.command
def assign_collection(collection_id):
    users = User.query.all()
    collection = Collection.query.filter_by(id=collection_id).first()

    if collection is None:
        print('Collection not found')
        return

    for user in users:
        owns_collection = OwnedCollection.query.filter_by(
            user_id=user.id, collection_id=collection.id).first()

        if owns_collection is None:
            collection.set_owner(user.id)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run()
