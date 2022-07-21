from pysnmp.hlapi import *



def get_mac_vlan_port(address):
	macs = []
	for (errorIndication, errorStatus, errorIndex, varBinds) in bulkCmd(
			SnmpEngine(), 
			CommunityData('public'),
			UdpTransportTarget((address, 161)), 
			ContextData(), 
			0, 25, 
			ObjectType(ObjectIdentity('1.3.6.1.4.1.34592.1.3.4.10.2.1.2.1.4')),
			lexicographicMode=False, lookupMib=True): 
		if errorIndication:
			return {'code':1, 'error':errorIndication}
		elif errorStatus:
			return {'code':2, 'error':errorIndication}
		else:
			ttt = list()
			for varBind in varBinds:
				# print(varBind[0].prettyPrint())
				t = varBind[1].prettyPrint()
				macs.append([varBind[0][15:16].prettyPrint(),varBind[0][16:17].prettyPrint(), t.replace('0x', '')])
	return {'code': 0, 'result': macs}
