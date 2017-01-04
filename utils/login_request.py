#coding:utf-8

# 必须先登录，否则跳转到/login

import functools
from flask import Flask,redirect,session

def login_request(func):
    @functools.wraps(func)
    def wrapper(*args,**kwargs):
	name = session.get('name')
	if not name:
	    return redirect('/login')
	else:
	    return func(*args,**kwargs)
    return wrapper
