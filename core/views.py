from flask import Blueprint, render_template, request, redirect, url_for
from .models import Router, subs_onu, Sub, Olt
from ..database import db


core = Blueprint('core', __name__, template_folder='templates', static_folder='static')


@core.route('/')
def index():
	abon = db.session.query(Sub).all()
	onu = db.session.query(subs_onu).all()
	data = []
	count = 0
	for i in abon:
		count = count + 1
		for n in onu:
			if i.login == n.subs_login:
				data.append([count, i.login, i.address, i.old_address, n.onu_mac, i.tvbox])
	return render_template('index/index.html', data = data)


@core.route('/update/<data>')
def update(data):
	#print(data)
	reqs_all_dev(int(data))
	return redirect(url_for('index'))



@core.route('/add_router', methods=['GET', 'POST'])
def add_router():

	if request.method == 'POST':

		name = request.form.get('name')
		login = request.form.get('login')
		password = request.form.get('password')
		ip = request.form.get('ip')
		port = request.form.get('port')

		db.session.add(Router(name, login, password, ip, port))
		db.session.commit()
		return render_template('add_router.html')


	return render_template('add_router.html')


@core.route('/add_olt', methods=['GET', 'POST'])
def add_olt():

	parents_hosts = db.session.query(Router).all()

	if request.method == 'POST':

		name = request.form.get('name')
		ip = request.form.get('ip')
		port = request.form.get('port')
		community = request.form.get('community')
		count_pon = request.form.get('count_pon')
		ros = request.form.get('parent_host')

		db.session.add(Olt(name, ip, ros))
		db.session.commit()
		return render_template('add_olt.html')


	return render_template('add_olt.html', parents_hosts = parents_hosts)



@core.route('/dev_list', methods=['GET', 'POST'])
def dev_list():
	routers_list = db.session.query(Router).all()
	olts_list = db.session.query(Olt).all()

	return render_template('dev_list.html', routers_list=routers_list, olts_list=olts_list)