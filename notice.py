#coding=utf-8
import requests
import json
import time
import hmac
import hashlib
import base64
import urllib

def sendDingDing(text):
	timestamp = long(round(time.time() * 1000))
	secret = 'secret'
	secret_enc = bytes(secret).encode('utf-8')
	string_to_sign = '{}\n{}'.format(timestamp, secret)
	string_to_sign_enc = bytes(string_to_sign).encode('utf-8')
	hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
	sign = urllib.quote_plus(base64.b64encode(hmac_code))
	print(timestamp)
	print(sign)

	url = "https://oapi.dingtalk.com/robot/send?access_token=xxxxxx&timestamp="+str(timestamp)+"&sign="+sign

	header = {
		"Content-Type": "application/json",
		"Charset": "UTF-8"
	}

	data = {
		"msgtype": "text",
		"text": {
			"content": text
		},
	}

	res=requests.post(url, data=json.dumps(data), headers=header)
