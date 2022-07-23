from pysnmp.hlapi import *
from app import db, Routers, Olts, Onu, Subs
from ros_api import get_username_mac


def get_mac_vlan_port(address, community, port, int_count):
	macs = []
	for i in range(1,int_count+1):
		for (errorIndication, errorStatus, errorIndex, varBinds) in bulkCmd(
				SnmpEngine(), 
				CommunityData(community),
				UdpTransportTarget((address, port)), 
				ContextData(), 
				0, 25, 
				ObjectType(
					ObjectIdentity(
						'1.3.6.1.4.1.34592.1.3.4.10.2.1.2.1.{}'.format(i)
						)
					),
				lexicographicMode=False, lookupMib=True): 
			if errorIndication:
				return {'code':1, 'error':errorIndication}
			elif errorStatus:
				return {'code':2, 'error':errorStatus}
			else:
				ttt = list()
				for varBind in varBinds:
					# print(varBind[0].prettyPrint())
					t = varBind[1].prettyPrint()
					macs.append([int(varBind[0][15:16].prettyPrint()), int(varBind[0][16:17].prettyPrint()), t.replace('0x', '')])
	return {'code': 0, 'result': macs}


def get_mac_vlan_port_1(address, community, port, int_count):
	macs = []
	for i in range(1,int_count+1):
		for (errorIndication, errorStatus, errorIndex, varBinds) in bulkCmd(
				SnmpEngine(), 
				CommunityData(community),
				UdpTransportTarget((address, port)), 
				ContextData(), 
				0, 25, 
				ObjectType(
					ObjectIdentity(
						'1.3.6.1.4.1.34592.1.3.4.1.1.7.1.{}'.format(i)
						)
					),
				lexicographicMode=False, lookupMib=True): 
			if errorIndication:
				return {'code':1, 'error':errorIndication}
			elif errorStatus:
				return {'code':2, 'error':errorStatus}
			else:
				ttt = list()
				for varBind in varBinds:
					t = varBind[1].prettyPrint()
					macs.append([i, int(varBind[0][15:16].prettyPrint()), t.replace('0x', '')])
	return {'code': 0, 'result': macs}



def reqs():

	#print(get_mac_vlan_port('192.168.250.18', 'public', 161, 4))

	routers = db.session.query(Routers).all()
	olts = db.session.query(Olts).all()

	for rt in routers:
		usr = get_username_mac(rt.ip, rt.login, rt.password)
		for olt in olts:
			if olt.ros == rt.id:
				onu = get_mac_vlan_port(olt.ip, olt.community, olt.port, olt.count_pon)
				onu1 = get_mac_vlan_port_1(olt.ip, olt.community, olt.port, olt.count_pon)
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
								print(
									n[0], n[1], n[2], "-", i[0],
									i[1].replace(':', '').lower(), nn[0], nn[1],nn[2]
									)



"""				print(usr, '\n\n')
				print(onu, '\n\n')
				print(onu1, '\n\n')"""



	#return rt


reqs()