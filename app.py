#coding=utf-8
from flask import Flask, redirect, request, make_response, session, render_template
from flask_cors import CORS
import json
import os
import time
from redis import Redis
import env
import code
import build
import publish
app = Flask(__name__, static_folder="static")
CORS(app, support_credentials=True)

from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor(1)
import notice
rs = Redis(host='127.0.0.1',port=6379,db=0,decode_responses=True)

@app.route('/')
def hello():
	return render_template("index.html")

@app.route('/buildfinish')
def buildfinish():
	rs.set("bazy", 0)
	response = make_response(json.dumps({"code":200, "msg":"success"}))
	return response 

@app.route('/package')
def package():
	isBazy = rs.get("bazy")
	if int(isBazy) == 1:
		response = make_response(json.dumps({"code":201, "msg":"打包中"}))
		return response
	name = request.args["name"]
	workspace = request.args["workspace"]
	buildtype = request.args["buildtype"]
	if os.path.exists(workspace) == False:
		return make_response(json.dumps({"code":201, "msg":"workspace not exist"}))
	rs.set("bazy", 1)
	executor.submit(doTask, name, workspace, buildtype)
	response = make_response(json.dumps({"code":200, "msg":"success"}))
	return response 

	
def doTask(name, workspace, buildtype):
	try:
		rs.set("bazy", 0)
	except IOError as e:
		print(e)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=6001, debug=True)


