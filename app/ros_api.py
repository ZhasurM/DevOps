import routeros_api
from routeros_api import RouterOsApiPool, exceptions
import numpy as np

import os



def get_username_mac(mik_ip, username, password):
	try:
		print(mik_ip, username, password)
		connection = RouterOsApiPool(mik_ip, username, password, port=8728, 
											  plaintext_login=True)
		data_array = []
		try:
			api = connection.get_api()
			#print(api)
			data = api.get_resource('/ppp/active')
			for dt in data.get():
				data_array.append([dt.get('name'), dt.get('caller-id')])
			return {'code':0, 'result': data_array}
		except routeros_api.exceptions.RouterOsApiCommunicationError:
			return {'code': 1, 'error':'RouterOsApiCommunicationError'} 
	except routeros_api.exceptions.RouterOsApiConnectionError:
		return {'code': 2, 'error':'RouterOsApiConnectionError'}


