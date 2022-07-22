from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1111@localhost:5432/test'
db = SQLAlchemy(app)

migrate = Migrate(app,db)


subs_onu = db.Table('subs_onu',
	db.Column('subs_login', db.String(), db.ForeignKey('subs.login')),
	db.Column('onu_mac', db.String(), db.ForeignKey('onu.mac')),
	db.Column('date', db.String(), server_default=str(datetime.datetime.now()))
	)


class Subs(db.Model):

	__tablename__ = 'subs'

	#id = db.Column(db.Integer, primary_key=True)
	login = db.Column(db.String(), primary_key=True)
	address = db.Column(db.String())
	old_address = db.Column(db.String())
	onus = db.relationship(
		'Onu', 
		secondary=subs_onu,
		backref=db.backref('subs', lazy='dynamic')
        )
	tvbox = db.Column(db.String())

	def __init__(self, login, address, old_address):
		self.login = login
		self.address = address
		self.old_address = old_address


class Onu(db.Model):

	__tablename__ = 'onu'

	mac = db.Column(db.String(), primary_key=True)
	owner = db.Column(db.String(), db.ForeignKey('subs.login'))

	def __init__(self, mac, ros):
		
		self.mac = mac
		self.ros = ros




class Routers(db.Model):

	__tablename__ = 'routers'

	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(), unique=True)
	login = db.Column(db.String())
	password = db.Column(db.String())
	ip = db.Column(db.String(), unique=True)
	port = db.Column(db.String())
	olt_id = db.relationship('Olts', backref='olt')


	def __init__(self, name, login, password, ip, port):
		self.name = name
		self.login = login
		self.password = password
		self.ip = ip
		self.port = port


class Olts(db.Model):

	__tablename__ = 'olts'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(), unique=True)
	login = db.Column(db.String())
	password = db.Column(db.String())
	ip = db.Column(db.String(), unique=True)
	ros = db.Column(db.Integer(), db.ForeignKey('routers.id'))

	def __init__(self, name, login, password, ip, ros):
		
		self.name = name
		self.login = login
		self.password = password
		self.ip = ip
		self.ros = ros



@app.route('/')
def index():
	return render_template('index/index.html')


@app.route('/add_dev', methods=['GET', 'POST'])
def add_dev():

	parents_hosts = db.session.query(Routers).all()

	if request.method == 'POST':
		node = request.form.get('type_host')
		name = request.form.get('name')
		login = request.form.get('login')
		password = request.form.get('password')
		ip = request.form.get('ip')
		port = request.form.get('port')
		ros = request.form.get('parent_host')

		if node == 'router':
			db.session.add(Routers(name, login, password, ip, port))
		else:
			db.session.add(Olts(name, login, password, ip, ros))
		print(ros)
		db.session.commit()
		return render_template('add_dev.html')


	return render_template('add_dev.html', parents_hosts = parents_hosts)



@app.route('/dev_list', methods=['GET', 'POST'])
def dev_list():
	routers_list = db.session.query(Routers).all()
	olts_list = db.session.query(Olts).all()

	return render_template('dev_list.html', routers_list=routers_list, olts_list=olts_list)


if __name__ == '__main__':
	app.run()
