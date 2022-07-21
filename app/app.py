from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1111@localhost:5432/test'
db = SQLAlchemy(app)

migrate = Migrate(app,db)


class Subs(db.Model):

	__tablename__ = 'subs'

	id = db.Column(db.Integer, primary_key=True)
	login = db.Column(db.String())
	address = db.Column(db.String())
	old_address = db.Column(db.String())
	onu = db.Column(db.String())
	tvbox = db.Column(db.String())


	def __init__(self, id, login, address, old_address, onu, tvbox):
		self.id = id
		self.login = login
		self.address = address
		self.old_address = address
		self.onu = onu
		self.tvbox = tvbox


class Routers(db.Model):

	__tablename__ = 'routers'

	id = db.Column(db.Integer, primary_key=True)
	login = db.Column(db.String())
	password = db.Column(db.String())
	ip = db.Column(db.String(), unique=True)
	port = db.Column(db.String())
	olt_id = db.relationship('Olts', backref='olt')


	def __init__(self, id, login, password, ip):
		self.id = id
		self.login = login
		self.password = password
		self.ip = ip


class Olts(db.Model):

	__tablename__ = 'olts'

	id = db.Column(db.Integer, primary_key=True)
	login = db.Column(db.String())
	password = db.Column(db.String())
	ip = db.Column(db.String(), unique=True)
	ros = db.Column(db.Integer(), db.ForeignKey('routers.id'))

	def __init__(self, id, login, password, ip):
		self.id = id
		self.login = login
		self.password = password
		self.ip = ip



@app.route('/')
def index():
	return render_template('index/index.html')


@app.route('/add_dev', methods=['GET', 'POST'])
def admin_ch():
	return render_template('admin.html')



if __name__ == '__main__':
	app.run()
