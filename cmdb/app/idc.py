#!/usr/bin/python
#coding:utf-8

from flask import render_template,request,redirect,session
from . import app
from config import *
from utils import login_request
import json
import db

app.config.from_object(Table)
fields_idc=app.config.get('FIELDS_IDC')

@app.route('/idc/')
@login_request.login_request
def idc():
    role = session.get('role')
    idcs = db.list('idc',fields_idc)
    return render_template("/idc/idclist.html",idcs = idcs,role = role)

@app.route('/idc_msg/')
@login_request.login_request
def idc_msg():
    idcs = db.list('idc',fields_idc)
    return json.dumps({'result':idcs}) 

@app.route("/idcadd/",methods=['GET','POST'])
@login_request.login_request
def idcadd():
    if request.method == 'GET':
	return render_template('/idc/idcadd.html',info = session,role = session.get('role'))
    if request.method == 'POST':
	data = dict((k,v[0]) for k,v in dict(request.form).items())
	l = []

	for i in db.list('idc',fields_idc):
	    l.append(i['name'])
	if not data['name']:
	    return json.dumps({'code':1,'errmsg':'name can not be null'})
	elif data['name'] not in l:
	    conditions = [ "%s='%s'" %  (k,v) for k,v in data.items()]
	    db.add('idc',conditions)
	    return json.dumps({'code':0,'result':'add idc success'})
	return json.dumps({'code':1,'errmsg':'idc name is exist'})

@app.route('/idc_update_msg/')
@login_request.login_request
def idc_update_msg():
    id = request.args.get('id')
    idc = db.list('idc',fields_idc,id)
    return json.dumps({'code':0,'result':idc})

@app.route('/idc_update/',methods=['GET','POST'])
@login_request.login_request
def idc_update():
    data = dict((k,v[0]) for k,v in dict(request.form).items())
    conditions = [ "%s='%s'" %  (k,v) for k,v in data.items()]
    db.update('idc',conditions,data['id'])
    return json.dumps({'code':0,'result':'update completed!'})

@app.route('/idc_delete/',methods=['POST'])
@login_request.login_request
def idc_delete():
    id = request.form.get('id')
    db.delete('idc',id)
    return json.dumps({'code':0,'result':'delete success!'})
