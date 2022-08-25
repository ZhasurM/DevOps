from flask import Flask
import os
import time
from sqlalchemy.exc import OperationalError
#from .config import DevelopmentConfig

from .database import db, migrate
from .core.views import core
from .log import logger


def create_app():
	app = Flask(__name__)
	app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
	app.config['FLASK_RUN_HOST'] = os.getenv('FLASK_RUN_HOST')
	#app.config['SERVER_NAME'] = "0.0.0.0"
	db.init_app(app)
	logger.info('Program started')
	cn = True
	logger.info('Test connect with database')
	for i in range(1, 11):
		try:
			with app.test_request_context():
				db.create_all()
		except OperationalError as er:
			cn = False
			logger.warning('Try = {}, Error = {}'.format(i, er))
			time.sleep(10)
		if cn == True:
			break
		if i == 10:
			logger.warning('Database error')
	migrate.init_app(app, db)

	app.register_blueprint(core)

	return app
