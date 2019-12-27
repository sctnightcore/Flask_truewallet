import json, requests, time, hmac, datetime
import hashlib
import hmac
from datetime import datetime, timedelta
from requests_toolbelt.utils import dump

key = "9LXAVCxcITaABNK48pAVgc4muuTNJ4enIKS5YzKyGZ".encode('utf-8')
def RequestLoginOTP(email, password):
	timestamp = round(time.time() * 1000)
	signature = hmac.new(key,'email|26099f131ecebab0|{}'.format(timestamp).encode('utf-8'), hashlib.sha1).hexdigest()
	header_data = {
		'Host': 'mobile-api-gateway.truemoney.com',
		'username': str(email),
		'password': str(hashlib.sha1((email+password).encode('utf-8')).hexdigest()),
		'Content-Type': 'application/json',
		'User-agent': 'okhttp/3.8.0'
	}
	json_data = {
		'type': 'email',
		'device_id': '26099f131ecebab0',
		'timestamp': str(timestamp),
		'signature' : str(signature)
	}
	try:
		r = requests.post("https://mobile-api-gateway.truemoney.com/mobile-api-gateway/api/v1/login/otp/", json=json_data, headers=header_data)
		if r.status_code == 200:
			return r.json()
		else:
			return r.json()
	except Exception as e:
		return False

def SubmitLoginOTP(email, password, otp_code, mobile_number, otp_reference):
	timestamp = round(time.time() * 1000)
	info = 'email|{}|{}|{}|26099f131ecebab0|DVOkkBrMoI2V9bTp3hzmhgRdENJUI2a7zHLAmxKAmuvipASQ==|{}'.format(otp_code,mobile_number,otp_reference,timestamp).encode('utf-8')
	signature = hmac.new(key, info, hashlib.sha1).hexdigest()
	header_data = {
		'Host': 'mobile-api-gateway.truemoney.com',
		'username': str(email),
		'password': str(hashlib.sha1((email+password).encode('utf-8')).hexdigest()),
		'Content-Type': 'application/json',
		'User-agent': 'okhttp/3.8.0'
	}
	json_data = {
		'type': 'email',
		'otp_code': str(otp_code),
		'mobile_number': str(mobile_number),
		'otp_reference': str(otp_reference),
		'device_id': '26099f131ecebab0',
		'mobile_tracking': 'DVOkkBrMoI2V9bTp3hzmhgRdENJUI2a7zHLAmxKAmuvipASQ==',
		'timestamp': str(timestamp),
		'signature' : str(signature)
	}
	try:
		r = requests.post("https://mobile-api-gateway.truemoney.com/mobile-api-gateway/api/v1/login/otp/verification", json=json_data, headers=header_data)
		if r.status_code == 200:
			return r.json()
		else:
			return r.json()
	except Exception as e:
		return False

def GetProfile(token):
	header_data = {
		'User-agent': 'okhttp/3.8.0',
		'Authorization': token
	}
	try:
		r = requests.get("https://mobile-api-gateway.truemoney.com/mobile-api-gateway/user-profile-composite/v1/users/",headers=header_data)
		if r.status_code == 200:
			return r.json()
		else:
			return r.json()
	except Exception as e:
		return False
def GetTransaction(token):
	header_data = {
		'User-agent': 'okhttp/3.8.0',
		'Authorization': token
	}
	try:
		enddate = datetime.now().date() - timedelta(days=-30)
		startdate = datetime.now().date() - timedelta(days=+90)
		limit = 50
		params_data = {
			'start_date': str(startdate),
			'end_date': str(enddate),
			'limit': int(limit)
		}
		r = requests.get("https://mobile-api-gateway.truemoney.com/mobile-api-gateway/user-profile-composite/v1/users/transactions/history", headers=header_data, params=params_data)
		if r.status_code == 200:
			return r.json()
		else:
			return r.json()
	except Exception as e:
		return False