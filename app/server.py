#!/usr/bin/python
#coding:utf-8

from flask import render_template,request,redirect,session
from . import app
from config import *
from utils import login_request
import json
import db

app.config.from_object(Table)
fields_cabinet=app.config.get('FIELDS_CABINET')  
fields_server=app.config.get('FIELDS_SERVER')  

@app.route('/server/')
@login_request.login_request
def server():
    role = session.get('role')
    servers = db.list('server',fields_server)
    for i in servers:
	cabinet = db.list('cabinet',fields_cabinet,i['cabinet_id'])
	i['cabinet_id'] = cabinet['name']

    return render_template("/server/serverlist.html",servers = servers,role = role)

@app.route("/serveradd/",methods=['GET','POST'])
@login_request.login_request
def serveradd():
    if request.method == 'GET':
	return render_template('/server/serveradd.html',info = session,role = session.get('role'))
    if request.method == 'POST':
	data = dict((k,v[0]) for k,v in dict(request.form).items())
	l = []

	for i in db.list('server',fields_server):
	    l.append(i['hostname'])
	if not data['hostname']:
	    return json.dumps({'code':1,'errmsg':'hostname can not be null'})
	elif data['hostname'] not in l:
	    conditions = [ "%s='%s'" %  (k,v) for k,v in data.items()]
	    db.add('server',conditions)
	    return json.dumps({'code':0,'result':'add server success'})
	return json.dumps({'code':1,'errmsg':'server name is exist'})

@app.route('/server_update_msg/')
@login_request.login_request
def server_update_msg():
    id = request.args.get('id')
    server = db.list('server',fields_server,id)
    return json.dumps({'code':0,'result':server})

@app.route('/server_update/',methods=['GET','POST'])
@login_request.login_request
def server_update():
    data = dict((k,v[0]) for k,v in dict(request.form).items())
    conditions = [ "%s='%s'" %  (k,v) for k,v in data.items()]
    db.update('server',conditions,data['id'])
    return json.dumps({'code':0,'result':'update completed!'})

@app.route('/server_delete/',methods=['POST'])
@login_request.login_request
def server_delete():
    id = request.form.get('id')
    db.delete('server',id)
    return json.dumps({'code':0,'result':'delete success!'})
