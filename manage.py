from app import create_app, db
from app.models.users import User
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand 
import os

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
Migrate = Migrate(app, db)

# initialize db migrate variable here

def make_shell_context():
	return dict(app=app, db=db, User=User)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
	manager.run()