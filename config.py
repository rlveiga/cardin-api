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

	SQLALCHEMY_DATABASE_URI = 'postgres://uiulrhslqdnhue:1da67cc96eda4402689b73925bcb01f6c3bde1b5bf7f3c66f55acdc54ecea930@ec2-54-165-36-134.compute-1.amazonaws.com:5432/d1cqcq6m3tet7j'

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
