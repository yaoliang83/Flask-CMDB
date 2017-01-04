#!/usr/bin/python
#coding:utf-8

from flask import render_template,request,redirect,session
from . import app
from hashlib import md5
from config import * 
from utils import login_request
from datetime import date
import json
import db,time

salt = '890iop*()'
app.config.from_object(Table)
fields_user = app.config.get('FIELDS_USER')

def duty(day): # 查看星期几的值班人的编号
    duty_dict = {}  # 带索引的值班人员字典
    duty_week = {}  # k: 星期几 ,v: 为list 值班人 ,v[0][1] 表示第二周的星期一
    duty_list = []  # 所有值班人员列表
    users = db.list('users',fields_user)
    for user in users:
	if user['role'] == 'admin' and user['status'] == 0:
	    duty_list.append(user['id'])
    duty_list *= 5
    duty_dict = { k:v for k,v in enumerate(duty_list)}
    for k,v in duty_dict.items():
	duty_week.setdefault(k,[])
	duty_week[k%5].append(v)

    week_num = (int(time.strftime('%W')))%(int(len(duty_list))/5) # 第几个星期 , 'int(len(duty_list))/5'周重置一次
    return duty_week[day][week_num]

@app.route("/dutyself/")
@login_request.login_request
def dutyself():
    today = date.weekday(date.today()) # 今天是星期几
    id = duty(today) 

    user = db.list('users',fields_user,id)
    role = session.get('role')
    return render_template("/duty/dutyself.html",user = user,role = role)
    
@app.route('/dutylist/')
@login_request.login_request
def dutylist():
    every_week = [] # 每周值班人汇总
    role = session.get('role')
    for i in range(5):
        data = db.list('users',fields_user,duty(i))
	if i == 0:
	    data['week'] = '星期一'
	    data['id'] = i
	elif i == 1:
	    data['week'] = '星期二'
	    data['id'] = i
	elif i == 2:
	    data['week'] = '星期三'
	    data['id'] = i
	elif i == 3:
	    data['week'] = '星期四'
	    data['id'] = i
	else:
	    data['week'] = '星期五'
	    data['id'] = i
        every_week.append(data)
         
    return render_template("/duty/dutylist.html",users = every_week,role = role)
