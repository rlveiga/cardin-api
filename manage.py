from app import app, db, socketio
from app.models.user import User
from app.models.room import Room, RoomAssociation
from app.models.card import Card
from app.models.collection import Collection

import flask
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand 
from flask_socketio import SocketIO

import os

manager = Manager(app)
Migrate = Migrate(app, db)

def make_shell_context():
	return dict(app=app, db=db, User=User, Card=Card, Collection=Collection, Room=Room, RoomAssociation=RoomAssociation)

@manager.command
def run():
  socketio.run(app)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
	manager.run()