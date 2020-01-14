from app import create_app, db
from app.models.user import User
from app.models.room import Room, Association
from app.models.card import Card
from app.models.collection import Collection

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand 

import os

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
Migrate = Migrate(app, db)

def make_shell_context():
	return dict(app=app, db=db, User=User, Card=Card, Collection=Collection, Room=Room, Association=Association)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
	manager.run()