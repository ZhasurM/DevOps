import asyncio
from asyncio import open_connection
from base64 import b64decode
from hashlib import sha1
from json import dumps, loads
from logging import getLogger
from math import modf
from struct import pack, unpack
from time import time as get_time

from Crypto.Cipher import AES
import os



KEY_MK_1 = os.getenv('KEY_MK_1')
KEY_MK_2 = os.getenv('KEY_MK_2')
MK_HOST=os.getenv('MK_HOST')
MK_LOGIN=os.getenv('MK_LOGIN')
MK_PASSWORD=os.getenv('MK_PASSWORD')



class MikroBILL:
    def __init__(self, login: str, password: str, host: str, port: int, key1: str, key2: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._login = login
        self._password = password
        self._host = host
        self._port = port
        self._key1 = b64decode(key1)
        self._key2 = b64decode(key2)
        self._reader = None
        self._writer = None
        self.logger = getLogger(__name__)

    async def auth(self):
        mt = '%f %d' % modf(get_time())
        auth = dumps({'auth': {'login': self._login,
                               'password': sha1("{}{}".format(self._password, mt).encode("utf-8")).hexdigest(),
                               'sign': mt
                               }})
        self._reader, self._writer = await open_connection(self._host, self._port)
        result = await self.send(auth)
        return dict(result)

    async def send(self, json):
        msg = self.mb_encrypt(json)
        self._writer.write(pack('I', len(msg)))
        self._writer.write(msg)
        await self._writer.drain()
        data_len = await self._reader.read(4)
        if '' != data_len.decode('unicode-escape'):
            full_len = unpack('I', data_len)
            full_len = full_len[0]
            data = await self._reader.read(full_len)
            result = self.mb_decrypt(data).decode().strip(b'\x00'.decode())
        else:
            result = '{"error": "РџСѓСЃС‚РѕР№ РѕС‚РІРµС‚", "code": "4"}'
            self._writer.close()
        return loads(result)

    async def process(self, path, value):
        json = dumps({'path': path, 'value': value})
        result = await self.send(json)
        return result

    def mb_encrypt(self, msg):
        crypto_bl = AES.new(self._key1, AES.MODE_CBC, IV=self._key2)
        data = msg.ljust(256, b'\x00'.decode()).encode()
        return crypto_bl.encrypt(data)

    def mb_decrypt(self, msg):
        crypto_bl = AES.new(self._key1, AES.MODE_CBC, IV=self._key2)
        return crypto_bl.decrypt(msg)

#
async def get_user_info(user_login):

    key1 = KEY_MK_1
    key2 = KEY_MK_2
    host = MK_HOST
    # TODO РџРѕСЂС‚ php api
    port = 7403
    # TODO РєР°СЃСЃРёСЂСѓ РґРѕР»Р¶РЅРѕ Р±С‹С‚СЊ СЂР°Р·СЂРµС€РµРЅРѕ РїРѕР»СЊР·РѕРІР°С‚СЊСЃСЏ php api
    login = MK_LOGIN
    password = MK_PASSWORD

    mbclient = MikroBILL(login, password, host, port, key1, key2)
    auth = await mbclient.auth()
    if auth.get('code') == 0:
        result = await mbclient.process('API.GetClients', user_login)
        if result.get('code') == 0:
            user_guid = str(result.get('return')[0])
            print(result)
            res = await mbclient.process('API.Client.{}.AutorizeInfo.Accounts'.format(user_guid), None)
            acc = res.get('return')[0]
            login_acc = await mbclient.process('API.Client.{}.AutorizeInfo.Accounts.{}.Login'.format(user_guid, acc), None)  
            #res = await mbclient.process('API.Client.{}.PersonalDataInfo.Fields'.format(user_guid), None)
            login_pass = await mbclient.process('API.Client.{}.AutorizeInfo.Accounts.{}.Password'.format(user_guid, acc), None)
            user_ip = await mbclient.process('API.Client.{}.AutorizeInfo.Accounts.{}.IP'.format(user_guid, acc), None)
            ppp_ip = await mbclient.process('API.Client.{}.AutorizeInfo.Accounts.{}.PPP_IP'.format(user_guid, acc), None)
            user_status = await mbclient.process('API.Client.{}.StatusInfo.Blocked'.format(user_guid), None)
            #user_group = await mbclient.process('API.Client.{}.BillingInfo.Group')

            return {'code':'0', 'login':login_acc['return'], 'password':login_pass['return'], 
                    'user_ip':user_ip['return'], 'ppp_ip': ppp_ip['return'], 'user_status': user_status['return']}
        else: 
            return {'code':'1'}
        await mbclient.process('DISCONNECT', None)
    else:
        return {'code':'1'}




async def get_address_from_mb(user_login):
    key1 = KEY_MK_1
    key2 = KEY_MK_2
    host = MK_HOST
    # TODO РџРѕСЂС‚ php api
    port = 7403
    # TODO РєР°СЃСЃРёСЂСѓ РґРѕР»Р¶РЅРѕ Р±С‹С‚СЊ СЂР°Р·СЂРµС€РµРЅРѕ РїРѕР»СЊР·РѕРІР°С‚СЊСЃСЏ php api
    login = MK_LOGIN
    password = MK_PASSWORD

    mbclient = MikroBILL(login, password, host, port, key1, key2)
    auth = await mbclient.auth()
    if auth.get('code') == 0:
        result = await mbclient.process('API.GetClients', user_login)
        if result.get('code') == 0:
            user_guid = str(result.get('return')[0])
            address = await mbclient.process('API.Client.{}.PersonalDataInfo.Address'.format(user_guid), None)
            old_address_field = await mbclient.process('API.Client.{}.PersonalDataInfo.Fields'.format(user_guid), None)
            for i in old_address_field.get('return'):
                old_address = await mbclient.process('API.Client.{}.PersonalDataInfo.Field.{}.FieldName'.format(user_guid, str(i)), None)
                if old_address['return'] == 'Address_Old':
                    user_old_address = await mbclient.process(
                            'API.Client.{}.PersonalDataInfo.Field.{}.FieldValue'.format(user_guid, str(i)), None)
            return address['return'] + user_old_address['return']
        	
        	











async def get_user_info_mk(user_login):

    key1 = KEY_MK_1
    key2 = KEY_MK_2
    host = MK_HOST
    print(host)
    # TODO РџРѕСЂС‚ php api
    port = 7403
    # TODO РєР°СЃСЃРёСЂСѓ РґРѕР»Р¶РЅРѕ Р±С‹С‚СЊ СЂР°Р·СЂРµС€РµРЅРѕ РїРѕР»СЊР·РѕРІР°С‚СЊСЃСЏ php api
    login = MK_LOGIN
    password = MK_PASSWORD

    mbclient = MikroBILL(login, password, host, port, key1, key2)
    auth = await mbclient.auth()
    if auth.get('code') == 0:
        result = await mbclient.process('API.GetClients', user_login)
        if result.get('code') == 0:
            user_guid = str(result.get('return')[0])
            res = await mbclient.process('API.Client.{}.AutorizeInfo.Accounts'.format(user_guid), None)
            acc = res.get('return')[0]
            # Логин
            login_acc = await mbclient.process('API.Client.{}.AutorizeInfo.Accounts.{}.Login'.format(user_guid, acc), None)
            # Пароль
            login_pass = await mbclient.process('API.Client.{}.AutorizeInfo.Accounts.{}.Password'.format(user_guid, acc), None)
            # IP Адресс
            #user_ip = await mbclient.process('API.Client.{}.AutorizeInfo.Accounts.{}.IP'.format(user_guid, acc), None)
            # IP для ppp
            #ppp_ip = await mbclient.process('API.Client.{}.AutorizeInfo.Accounts.{}.PPP_IP'.format(user_guid, acc), None)
            # статус аккаунта
            #user_status = await mbclient.process('API.Client.{}.StatusInfo.Blocked'.format(user_guid), None)
            # Tриф
            #tarif = await mbclient.process('API.Client.{}.BillingInfo.Tariff'.format(user_guid), None)
            # группа 
            #user_group = await mbclient.process('API.Client.{}.BillingInfo.Group'.format(user_guid), None)
            # Адрес
            address = await mbclient.process('API.Client.{}.PersonalDataInfo.Address'.format(user_guid), None)
            # Номер телефона
            mobile_tel = await mbclient.process('API.Client.{}.PersonalDataInfo.MobileTel'.format(user_guid), None)
            # ID поля Address_old
            old_address_field = await mbclient.process('API.Client.{}.PersonalDataInfo.Fields'.format(user_guid), None)

            for i in old_address_field.get('return'):
                old_address = await mbclient.process('API.Client.{}.PersonalDataInfo.Field.{}.FieldName'.format(user_guid, str(i)), None)
                if old_address['return'] == 'Address_Old':
                    user_old_address = await mbclient.process(
                            'API.Client.{}.PersonalDataInfo.Field.{}.FieldValue'.format(user_guid, str(i)), None)
            return {'code':0, 'login':login_acc['return'], 'password':login_pass['return'],
                    'address': address['return'], 'old_address': user_old_address['return'],
                    'mobile_tel': mobile_tel['return']}
#            return {'code':0, 'login':login_acc['return'], 'password':login_pass['return'], 
#                    'user_ip':user_ip['return'], 'ppp_ip': ppp_ip['return'], 'user_status': user_status['return'],
#                    'tarif': tarif['return'], 'address': address['return'], 'old_address': user_old_address['return'],
#                    'mobile_tel': mobile_tel['return']}
        else: 
            return result
        await mbclient.process('DISCONNECT', None)
    else:
        return auth

