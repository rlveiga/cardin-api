import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to figure out long ass string'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True

	# Should set environment variables for database uri in the future

	SQLALCHEMY_DATABASE_URI = 'postgresql://rlveiga:@localhost/cardin_dev'

class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = 'postgresql://rlveiga:@localhost/cardin_test'

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = 'postgresql://rlveiga:@localhost/cardin_prod'

config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,

	'default': DevelopmentConfig
}
