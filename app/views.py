@app.route('/')
def index():
	abon = db.session.query(Subs).all()
	onu = db.session.query(subs_onu).all()
	data = []
	count = 0
	for i in abon:
		count = count + 1
		for n in onu:
			if i.login == n.subs_login:
				data.append([count, i.login, i.address, i.old_address, n.onu_mac, i.tvbox])
	return render_template('index/index.html', data = data)


@app.route('/update/<data>')
def update(data):
	print(data)
	reqs_all_dev(int(data))
	return redirect(url_for('index'))



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