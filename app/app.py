from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1111@localhost:5432/test'
db = SQLAlchemy(app)

migrate = Migrate(app,db)


class Subs(db.Model):

	__tablename__ = 'subs'

	id = db.Column(db.Integer, primary_key=True)
	login = db.Column(db.String(), unique=True)
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
def admin_ch():

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



if __name__ == '__main__':
	app.run()
