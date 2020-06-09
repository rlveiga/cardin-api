from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import config 

import os

def create_app(config_name):
  global db
  global ma
  global app
  global socketio

  db = SQLAlchemy()
  ma = Marshmallow()

  app = Flask(__name__, instance_relative_config=True)

  ma.init_app(app)

  app.config.from_object(config[config_name])
  config[config_name].init_app(app)

  # Creating SocketIO app here so that
  # it can be accessed by views
  socketio = SocketIO(app)

  db.init_app(app)

  from .auth import auth as auth_blueprint
  from .card import card as card_blueprint
  from .collection import collection as collection_blueprint
  from .collection import owned_collection as owned_collection_blueprint
  from .room import room as room_blueprint
  from .loader import loader as loader_blueprint

  app.register_blueprint(auth_blueprint)
  app.register_blueprint(card_blueprint)
  app.register_blueprint(collection_blueprint)
  app.register_blueprint(owned_collection_blueprint)
  app.register_blueprint(room_blueprint)
  app.register_blueprint(loader_blueprint)

  return app

create_app(os.environ.get('FLASK_CONFIG') or 'default')