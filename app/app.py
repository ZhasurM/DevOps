from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_migrate import Migrate
from ros_api import get_username_mac


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1111@localhost:5432/test'
db = SQLAlchemy(app)

migrate = Migrate(app,db)


subs_onu = db.Table('subs_onu',
	db.Column('subs_login', db.String(), db.ForeignKey('subs.login')),
	db.Column('onu_mac', db.String(), db.ForeignKey('onu.mac')),
	db.Column('date', db.String(), server_default=str(datetime.datetime.now()))
	)


subs_tvbox = db.Table('subs_tvbox',
	db.Column('subs_login', db.String(), db.ForeignKey('subs.login')),
	db.Column('tvbox_mac', db.String(), db.ForeignKey('tvbox.mac')),
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
	tvbox = db.relationship(
		'Tvbox', 
		secondary=subs_tvbox,
		backref=db.backref('subs', lazy='dynamic')
        )

	def __init__(self, login):
		self.login = login
		#self.address = address
		#self.old_address = old_address


class Onu(db.Model):

	__tablename__ = 'onu'

	mac = db.Column(db.String(), primary_key=True)
	interface = db.Column(db.Integer())
	pon_id = db.Column(db.Integer())
	signal = db.Column(db.Integer())
	owner = db.Column(db.String(), db.ForeignKey('subs.login'))
	olt = db.Column(db.Integer())

	def __init__(self, mac, interface, pon_id, olt):
		
		self.mac = mac
		self.interface = interface
		self.pon_id = pon_id
		self.olt = olt


class Tvbox(db.Model):

	__tablename__ = 'tvbox'

	mac = db.Column(db.String(), primary_key=True)
	owner = db.Column(db.String(), db.ForeignKey('subs.login'))

	def __init__(self, mac):

		self.mac = mac


def reqs():

	rt = db.session.query(Routers).all()
	olt = db.session.query(Olts).all()

	for r in rt:
		f = get_username_mac(r.ip, r.login, r.password)
		print(f)
		

	return rt





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
	ip = db.Column(db.String(), unique=True)
	port = db.Column(db.String())
	count_pon = db.Column(db.Integer())
	community = db.Column(db.String())
	ros = db.Column(db.Integer(), db.ForeignKey('routers.id'))


	def __init__(self, 
		name, 
		ip, 
		ros, 
		port = '161', 
		community = 'public',
		count_pon = 4
		):
		
		self.name = name
		self.ip = ip
		self.port = port
		self.ros = ros
		self.community = community
		self.count_pon = count_pon



@app.route('/')
def index():
	return render_template('index/index.html')


@app.route('/add_router', methods=['GET', 'POST'])
def add_router():

	if request.method == 'POST':

		name = request.form.get('name')
		login = request.form.get('login')
		password = request.form.get('password')
		ip = request.form.get('ip')
		port = request.form.get('port')

		db.session.add(Routers(name, login, password, ip, port))
		db.session.commit()
		return render_template('add_router.html')


	return render_template('add_router.html')


@app.route('/add_olt', methods=['GET', 'POST'])
def add_olt():

	parents_hosts = db.session.query(Routers).all()

	if request.method == 'POST':

		name = request.form.get('name')
		ip = request.form.get('ip')
		port = request.form.get('port')
		community = request.form.get('community')
		count_pon = request.form.get('count_pon')
		ros = request.form.get('parent_host')

		db.session.add(Olts(name, ip, ros))
		db.session.commit()
		return render_template('add_olt.html')


	return render_template('add_olt.html', parents_hosts = parents_hosts)



@app.route('/dev_list', methods=['GET', 'POST'])
def dev_list():
	routers_list = db.session.query(Routers).all()
	olts_list = db.session.query(Olts).all()

	return render_template('dev_list.html', routers_list=routers_list, olts_list=olts_list)


if __name__ == '__main__':
	app.run()
