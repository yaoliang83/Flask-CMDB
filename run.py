#!/usr/bin/python
#coding:utf-8

from app import app

if __name__=='__main__':
    app.run(host='0.0.0.0',port=8888,debug=True)
