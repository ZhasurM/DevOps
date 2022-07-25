from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
import datetime
from flask_migrate import Migrate
from ros_api import get_username_mac


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1111@localhost:5432/test'
db = SQLAlchemy(app)

migrate = Migrate(app,db)


if __name__ == '__main__':
	app.run(host='0.0.0.0')



# select subs.login, onu_mac from subs, subs_onu where subs.login = subs_onu.subs_login;