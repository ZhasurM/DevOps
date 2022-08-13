from flask import Flask
import os
#from .config import DevelopmentConfig

from .database import db, migrate
from .core.views import core


def create_app():
	app = Flask(__name__)
	app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
	app.config['FLASK_RUN_HOST'] = os.getenv('FLASK_RUN_HOST')
	#app.config['SERVER_NAME'] = "0.0.0.0"
	db.init_app(app)
	with app.test_request_context():
		db.create_all()
	
	migrate.init_app(app, db)

	app.register_blueprint(core)

	return app
