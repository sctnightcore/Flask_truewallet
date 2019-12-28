import os.path
import time
import requests
import hashlib
import hmac
import base64
from datetime import datetime, timedelta
import base64
import os
from requests_toolbelt.utils import dump

class Truewallet(object):
	def __init__(self, email=None, password=None):
		self.email = email
		self.password = password
		self.mobile_tracking = None
		self.device_id = None
		self.secret_key = "9LXAVCxcITaABNK48pAVgc4muuTNJ4enIKS5YzKyGZ".encode('utf-8')
		if self.mobile_tracking == None and self.device_id == None:
			if os.path.isfile("truewallet_identity.txt"):
				with open('truewallet_identity.txt', 'r') as File:
					data = File.read().splitlines()[0]
					self.device_id = data.split("|")[0]
					self.mobile_tracking = data.split("|")[1]
					File.close()
			else:
				with open('truewallet_identity.txt', 'w') as File:
					File.write(self.generate_identity())
					File.close()

	def generate_identity(self):
		self.mobile_tracking = base64.b64encode(os.urandom(40))
		self.device_id = hashlib.md5(self.mobile_tracking).hexdigest()
		return "{}|{}".format(self.device_id[0:16], self.mobile_tracking.decode())

	def setEmail_Password(self, email, password):
		self.email = email
		self.password = password
		self.password_enc = hashlib.sha1((self.email+self.password).encode('utf-8')).hexdigest()

	def getTimestamp(self):
		return str(round(time.time() * 1000))

	def RequestLoginOTP(self, email , password):
		self.setEmail_Password(email, password)
		timestamp = self.getTimestamp()
		info = "email|{}|{}".format(self.device_id, timestamp)
		signature = str(hmac.new(self.secret_key, info.encode('utf-8'), hashlib.sha1).hexdigest())
		try:
			r = requests.post("https://mobile-api-gateway.truemoney.com/mobile-api-gateway/api/v1/login/otp/", json={ 'type': 'email', 'device_id': self.device_id, 'timestamp': timestamp, 'signature': signature }, headers={ 'host': 'mobile-api-gateway.truemoney.com', 'username': self.email, 'password': self.password_enc, 'Content-Type': 'application/json', 'User-agent': 'okhttp/3.8.0'})
			if r.status_code == 200:
				return r.json()
			else:
				return r.json()
		except Exception as e:
			return False
	def SubmitLoginOTP(self, otp_code, mobile_number, otp_reference):
		timestamp = self.getTimestamp()
		info = '{}|{}|{}|{}|{}|{}|{}'.format("email" ,otp_code, mobile_number, otp_reference, self.device_id, self.mobile_tracking, timestamp)
		signature = str(hmac.new(self.secret_key, info.encode('utf-8'), hashlib.sha1).hexdigest())
		try:
			r = requests.post("https://mobile-api-gateway.truemoney.com/mobile-api-gateway/api/v1/login/otp/verification", json={ 'type': 'email', 'otp_code': otp_code, 'mobile_number': mobile_number, 'otp_reference': otp_reference, 'device_id': self.device_id, 'mobile_tracking': self.mobile_tracking, 'timestamp': timestamp, 'signature': signature}, headers={ 'Host': 'mobile-api-gateway.truemoney.com', 'username': self.email, 'password': self.password_enc, 'Content-Type': 'application/json', 'User-agent': 'okhttp/3.8.0'})
			if r.status_code == 200:
				return r.json()
			else:
				return r.json()
		except Exception as e:
			return False
	def GetProfile(self, token):
		try:
			r = requests.get("https://mobile-api-gateway.truemoney.com/mobile-api-gateway/user-profile-composite/v1/users/",headers={ 'User-agent': 'okhttp/3.8.0', 'Content-Type': 'application/json', 'Authorization': token})
			if r.status_code == 200:
				return r.json()
			else:
				return r.json()
		except Exception as e:
			return False
	def GetTransaction(self, token):
		startdate = datetime.now().date() - timedelta(days=+120)
		enddate = datetime.now().date() - timedelta(days=-30)
		limit = 50
		try:
			r = requests.get("https://mobile-api-gateway.truemoney.com/mobile-api-gateway/user-profile-composite/v1/users/transactions/history", headers={'User-agent': 'okhttp/3.8.0', 'Content-Type': 'application/json', 'Authorization': token}, params={'start_date': startdate, 'end_date': enddate, 'limit': limit})
			print(dump.dump_all(r))
			if r.status_code == 200:
				return r.json()
			else:
				return r.json()
		except Exception as e:
			return False

