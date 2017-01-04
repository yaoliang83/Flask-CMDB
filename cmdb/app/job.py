#!/usr/bin/python
#coding:utf-8

from flask import render_template,request,redirect,session
from threading import Thread
from . import app
from config import * 
from utils import login_request,myMail
from datetime import date
from duty import duty
import base64
import json
import db
import time

app.config.from_object(Table)
fields_job = app.config.get('FIELDS_OPS_JOBS')  
fields_user = app.config.get('FIELDS_USER')  
ISOTIMEFORMAT='%Y-%m-%d %X'

''' 
{'0':'未处理','1':'处理中','2':'完成','3':'失败'}
'''

# 获取值班人邮件地址和密码
today = date.weekday(date.today())
duty_email = db.list('users',fields_user,duty(today))['email']
duty_passwd = base64.b64decode(db.list('users',fields_user,duty(today))['email_password'])

@app.route('/joblist/')
@login_request.login_request
def joblist():
    role = session.get('role')
    jobs = db.list('ops_jobs',fields_job)
    list_jobs = []
    for job in jobs:
        if job['status'] == 0 or job['status'] == 1:
	    list_jobs.append(job)
    return render_template("/job/joblist.html",jobs = list_jobs,role = role)

@app.route('/jobhistory/')
@login_request.login_request
def jobhistory():
    role = session.get('role')
    jobs = db.list('ops_jobs',fields_job)
    history_jobs = []
    for job in jobs:
        if job['status'] == 2 or job['status'] == 3:
    	    history_jobs.append(job)
    return render_template("/job/jobhistory.html",jobs = history_jobs,role = role)

@app.route("/jobadd/",methods=['GET','POST'])
@login_request.login_request
def jobadd():
    name = session.get('name')
    id = session.get('id')
    if request.method == 'GET':
	return render_template('/job/jobadd.html',info = session,role = session.get('role'))
    else:
	data = dict((k,v[0]) for k,v in dict(request.form).items())
	data['apply_persion'] = name

	if not data['apply_desc']:
	    return json.dumps({'code':1,'errmsg':'job description can not be null'})
	conditions = [ "%s='%s'" %  (k,v) for k,v in data.items()]
	db.add('ops_jobs',conditions)

	# 获取申请人email地址
        user = db.list('users',fields_user,id)
	# 从用户列表获取邮箱账号和密码
        email,passwd = user['email'],base64.b64decode(user['email_password'])
	# 发送邮件(申请人发邮件给当天值班人)
	# myMail.myMail(email,passwd,duty_email,data['apply_desc'])
	# 异步发送
	thr = Thread(target=myMail.myMail,args=(email,passwd,duty_email,data['apply_desc']))
	thr.start()

	return json.dumps({'code':0,'result':'apply job success'})

# 获取工单状态
@app.route('/job_status/')
@login_request.login_request
def job_status():
    id = request.args.get('id')
    job = db.list('ops_jobs',fields_job,id)
#    return json.dumps({'code':0,'result1':apply_desc,'result2':status})
    result1 = job['status']
    result2 = job['apply_desc']
    result3 = job['deal_desc']
    return json.dumps({'code':0,'result1':result1,'result2':result2,'result3':result3})


# 修改工单状态
''' 
{'0':'未处理','1':'处理中','2':'完成','3':'失败'}
'''
@app.route('/update_status/',methods=['POST'])
@login_request.login_request
def update_status():
    data = dict((k,v[0]) for k,v in dict(request.form).items())
    job = db.list('ops_jobs',fields_job,data['id'])
    res = {}

    # 获取申请人信息
    users = db.list('users',fields_user)
    for user in users:
	if job['apply_persion'] == user['name']:
    # 获取值班人的邮箱
	    email = user['email']

    if data['status'] == '1':
	data['deal_persion'] = session.get('name')
	result = '申请已通过，请执行!'

	# 值班人执行操作后发邮件给工单申请人
	thr = Thread(target=myMail.myMail,args=(duty_email,duty_passwd,email,result))
	thr.start()
    else:
	data['deal_time'] = time.strftime(ISOTIMEFORMAT,time.localtime())

	if data['status'] == '2':
	    result = '工单处理正确，{}'.format(data['deal_desc'])
	else:
	    result = '工单失败，失败原因:{}'.format(data['deal_desc'])
	thr = Thread(target=myMail.myMail,args=(duty_email,duty_passwd,email,result))
	thr.start()

    conditions = [ "%s='%s'" %  (k,v) for k,v in data.items()]
    db.update('ops_jobs',conditions,data['id'])
    return json.dumps({'code':0,'result':'execute completed!'})

@app.route('/send_mail/',methods=['POST'])
@login_request.login_request
def send_mail():
    job_id = request.form.get('id')
    job = db.list('ops_jobs',fields_job,job_id)
    user = db.list('users',fields_user,session.get('id'))
    email,passwd = user['email'],base64.b64decode(user['email_password'])
    result = '申请时间: {},工单名: {} 已处理，请确认'.format(job['apply_date'],job['apply_type'])
    thr = Thread(target=myMail.myMail,args=(email,passwd,duty_email,result))
    thr.start()

    return json.dumps({'result':'send mail success!'})
