from routeros_api import RouterOsApiPool, exceptions
from ..log import logger
#import numpy as np




def get_username_mac(mik_ip, username, password):
	try:
		connection = RouterOsApiPool(mik_ip, username, password, port=8728, 
											  plaintext_login=True)
		data_array = []
		try:
			api = connection.get_api()
			#print(api)
			data = api.get_resource('/ppp/active')
			for dt in data.get():
				data_array.append([dt.get('name'), dt.get('caller-id')])
			logger.info('Request from {} succesfull'.format(mik_ip))
			return {'code':0, 'result': data_array}
		except exceptions.RouterOsApiCommunicationError as er:
			logger.error(er)
			return {'code': 1, 'error':er} 
	except exceptions.RouterOsApiConnectionError as er:
		logger.error(er)
		return {'code': 2, 'error':er}


