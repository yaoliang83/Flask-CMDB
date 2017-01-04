#!/usr/bin/python
#coding:utf-8

from flask import render_template,request,redirect,session
from . import app
from hashlib import md5
from config import *
from utils import login_request
import base64
import json
import db

salt = '890iop*()'
app.config.from_object(Table)
fields_user = app.config.get('FIELDS_USER')

@app.route('/')
@app.route('/index/')
@login_request.login_request
def index():
    role = session.get('role')
    return render_template('/base/index.html',role=role)


@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('/base/login.html')
    else:
	name = request.form.get('name')
	password = md5(request.form.get('password')+salt).hexdigest()

	d = {}
        for i in db.list('users',fields_user):
	    d[i['name']] = [i['password'],i['role'],i['id'],i['status']]
        if not name or not password:
	    errmsg = 'name or password not be null'
	    return json.dumps({'code':'1','errmsg':errmsg})
	elif d[name][3] != 0:
	    return json.dumps({'code':'1','errmsg':'user is locked'})

	elif name in d and d[name][0]==password:
	    session['name']=name
	    session['role']=d[name][1]
	    session['id']=d[name][2]
            return json.dumps({'code':'0','result':'login success'})
	else:
	    errmsg = 'name or password wrong'
	    return json.dumps({'code':'1','errmsg':errmsg})

@app.route("/userlist/")
@login_request.login_request
def userlist():
    role = session.get('role')
    if role == 'admin':
	users = db.list('users',fields_user)
	return render_template("/user/userlist.html",users = users,role = role)
    else:
        user = db.list('users',fields_user,session.get('id'))
        return render_template("/user/userself.html",user = user,role = role)

@app.route("/userself/")
@login_request.login_request
def userself():
    role = session.get('role')
    user = db.list('users',fields_user,session.get('id'))
    return render_template("/user/userself.html",user = user,role = role)

@app.route("/useradd/",methods=['GET','POST'])
@login_request.login_request
def useradd():
    if request.method == 'GET':
	return render_template('/user/add.html',role = session.get('role'))
    if request.method == 'POST':
	l = []
	data = dict((k,v[0]) for k,v in dict(request.form).items())
	data['password'] = md5(data['password']+salt).hexdigest()
	data['email_password'] = base64.b64encode(data['email_password'])

	for i in db.list('users',fields_user):
	    l.append(i['name'])
	if not data['name']:
	    return json.dumps({'code':1,'errmsg':'name can not be null'})
	elif not data['name_cn']:
	    return json.dumps({'code':1,'errmsg':'chinese name can not be null'})
	elif not data['password']:
	    return json.dumps({'code':1,'errmsg':'password can not be null'})
	elif data['name'] not in l:
	    conditions = [ "%s='%s'" %  (k,v) for k,v in data.items()]
	    db.add('users',conditions)
	    return json.dumps({'code':0,'result':'add user success'})
	return json.dumps({'code':1,'errmsg':'username is exist'})

@app.route('/modpwd/',methods=['POST'])
@login_request.login_request
def modpwd():
    data = dict(request.form)
    if 'password' in data.keys():
	if not data['password'][0] or not data['newpassword'][0] or not data['renewpassword'][0]:
	    errmsg = 'password can not be null'
	    return json.dumps({'code':'1','errmsg':errmsg})
    else:
	if not data['newpassword'][0] or not data['renewpassword'][0]:
	    errmsg = 'password can not be null'
	    return json.dumps({'code':'1','errmsg':errmsg})

    try:
	condition = [ "%s='%s'" %  ('password',md5(v[0]+salt).hexdigest()) for k,v in data.items() if k == 'newpassword']
	id = session.get('id')
	if session.get('role') == 'admin':
	    db.update('users',condition,data['id'][0])
	    return json.dumps({'code':'0','result':'modify completed!'})
	else:
	    if md5(data['password'][0]+salt).hexdigest() == db.list('users',fields_user,id)['password']:
		db.update('users',condition,data['id'][0])
		return json.dumps({'code':'0','result':'modify completed!'})
	    return json.dumps({'code':'1','errmsg':'wrong old password'})
    except:
	errmsg = "modify failed" 
	return json.dumps({'code':'1','errmsg':errmsg})

@app.route('/delete/',methods=['POST'])
@login_request.login_request
def delete():
    id = request.form.get('id')
    db.delete('users',id)
    return json.dumps({'code':0,'result':'delete success!'})


@app.route('/update_msg/')
@login_request.login_request
def update_msg():
    id = request.args.get('id')
    user = db.list('users',fields_user,id)
    user['email_password'] = base64.b64decode(user['email_password'])
    if session.get('role') == 'admin':
	return json.dumps({'code':0,'result':user})
    else:
	return json.dumps({'code':2,'result':user})

@app.route('/update/',methods=['GET','POST'])
@login_request.login_request
def update():
    data = dict((k,v[0]) for k,v in dict(request.form).items())
    data['email_password'] = base64.b64encode(data['email_password'])
    conditions = [ "%s='%s'" %  (k,v) for k,v in data.items()]
    db.update('users',conditions,data['id'])
    return json.dumps({'code':0,'result':'update completed!'})

@app.route('/logout/')
def loginout():
    if session:
	session.pop('role')
	session.pop('name')
	session.pop('id')
	return redirect('/login')
    return redirect('/login')
