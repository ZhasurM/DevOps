from flask import Flask
import os
#from .config import DevelopmentConfig

from .database import db, migrate
from .core.views import core


def create_app():
	app = Flask(__name__)
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1111@localhost:5432/test'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.init_app(app)
	migrate.init_app(app, db)
	with app.test_request_context():
		db.create_all()

	app.register_blueprint(core)

	return app