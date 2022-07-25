from app import db

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