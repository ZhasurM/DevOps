



def reqs_all_dev():

	try:
		routers = db.session.query(Routers).all()
		olts = db.session.query(Olts).all()

		for rt in routers:

			usr = get_username_mac(rt.ip, rt.login, rt.password)

			if usr['code'] == 1:
				return {'code': 1, 'result': usr['result']}

			for olt in olts:
				if olt.ros == rt.id:
					onu = get_mac_vlan_port(olt.ip, olt.community, olt.port, olt.count_pon)
					onu1 = get_mac_vlan_port_1(olt.ip, olt.community, olt.port, olt.count_pon)
					if onu['code'] == 1 or onu1['code'] == 1:
						return {'code': 1, 'result': 'olt_error'}
				for i in usr['result']:
					for n in onu['result']:
						if n[2] == i[1].replace(':', '').lower():
							for nn in onu1['result']:
								if n[0] == nn[0] and n[1] == nn[1]:
									us = Subs(i[0])
									on = Onu(nn[2], n[0], n[1], olt.id)
									db.session.merge(on)
									us.onus.append(on)
									db.session.merge(us)
									db.session.commit()

		return {'code': 0, 'result': 'succsesful'}
	except OperationalError as er:
		return {'code': 1, 'result': er}
	except psycopg2.OperationalError as e:
		return {'code': 1, 'result': e}