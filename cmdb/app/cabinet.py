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
fields_cabinet=app.config.get('FIELDS_CABINET')  

@app.route('/cabinet/')
@login_request.login_request
def cabinet():
    role = session.get('role')
    cabinets = db.list('cabinet',fields_cabinet)
    for i in cabinets:
	idc = db.list('idc',fields_idc,i['idc_id'])
	i['idc_id'] = idc['name']

    return render_template("/cabinet/cabinetlist.html",cabinets = cabinets,role = role)

@app.route('/cabinet_msg/')
@login_request.login_request
def cabinet_msg():
    cabinets = db.list('cabinet',fields_cabinet)
    return json.dumps({'result':cabinets}) 

@app.route("/cabinetadd/",methods=['GET','POST'])
@login_request.login_request
def cabinetadd():
    if request.method == 'GET':
	return render_template('/cabinet/cabinetadd.html',info = session,role = session.get('role'))
    if request.method == 'POST':
	data = dict((k,v[0]) for k,v in dict(request.form).items())
	l = []

	for i in db.list('cabinet',fields_cabinet):
	    l.append(i['name'])
	if not data['name']:
	    return json.dumps({'code':1,'errmsg':'name can not be null'})
	elif data['name'] not in l:
	    conditions = [ "%s='%s'" %  (k,v) for k,v in data.items()]
	    db.add('cabinet',conditions)
	    return json.dumps({'code':0,'result':'add cabinet success'})
	return json.dumps({'code':1,'errmsg':'cabinet name is exist'})

@app.route('/cabinet_update_msg/')
@login_request.login_request
def cabinet_update_msg():
    id = request.args.get('id')
    cabinet = db.list('cabinet',fields_cabinet,id)
    return json.dumps({'code':0,'result':cabinet})

@app.route('/cabinet_update/',methods=['GET','POST'])
@login_request.login_request
def cabinet_update():
    data = dict((k,v[0]) for k,v in dict(request.form).items())
    conditions = [ "%s='%s'" %  (k,v) for k,v in data.items()]
    db.update('cabinet',conditions,data['id'])
    return json.dumps({'code':0,'result':'update completed!'})

@app.route('/cabinet_delete/',methods=['POST'])
@login_request.login_request
def cabinet_delete():
    id = request.form.get('id')
    db.delete('cabinet',id)
    return json.dumps({'code':0,'result':'delete success!'})
