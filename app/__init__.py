from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import config 

db = SQLAlchemy()
ma = Marshmallow()

def create_app(config_name):
	app = Flask(__name__, instance_relative_config=True)

	ma.init_app(app)
	
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	db.init_app(app)

	from .main import main as main_blueprint

	app.register_blueprint(main_blueprint)

	return app