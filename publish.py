import shell
import requests
import os
def uploadBugly(buglyAppKey, buglyAppId, dysmZipPath, bundleId, version):
	url = "https://api.bugly.qq.com/openapi/file/upload/symbol"
	fileName = os.path.basename(dysmZipPath)
	params = {"api_version":1, "app_id":buglyAppKey, "app_key":buglyAppId, "symbolType":2, "bundleId":bundleId, "productVersion":version, "fileName":fileName}
	files = {"file":open(dysmZipPath, "rb")}
	res = requests.post(url, data=params, files=files)
	print(res.text)

def uploadFir(token, ipaPath):
	shell.run("fir login -T %s"%(token))
	shell.run("fir publish %s"%(ipaPath))

def uploadAppstore(ipaPath, apiKey, apiIssuer):
	shell.run("xcrun altool --upload-app -f %s -t ios --apiKey %s --apiIssuer %s --verbose"%(ipaPath, apiKey, apiIssuer))