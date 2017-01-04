#!/usr/bin/python
#coding:utf-8

from flask import Flask

app = Flask(__name__)
app.secret_key='\xd1\xfe\xfb\x7fH\xbf\xc8Q\x17-\xab\xc6\x80u2\xc2\xb6\n9\x00\x87\xa7\xa75'


import user,idc,cabinet,server,job,code,duty
