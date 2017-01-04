#coding:utf-8

import MySQLdb as mysql
from app import app
from config import *
from utils import logutil
import traceback
import sys

app.config.from_object(MysqlConfig)

host = app.config.get('SQL_HOST')
user = app.config.get('SQL_USER')
passwd = app.config.get('SQL_PASSWD')
db = app.config.get('SQL_DB')

conn = mysql.connect(user=user,passwd=passwd,host=host,db=db,charset='utf8')
conn.ping(True)
conn.autocommit(True)

with conn as cur:
    def list(table,fields,id=None):
	users = []
	if not id:
	    sql = "select %s from %s"%(','.join(fields),table)
	    try:
		logutil.writelog('db').info("sql: %s"%sql)
		cur.execute(sql)
		result = cur.fetchall()
		for row in result:
		    user = {}
		    for i,k in enumerate(fields):
			user[k] = row[i]
		    users.append(user)
		return users
	    except:
		logutil.writelog('db').error("Exec: %s,Error: %s"% (sql,traceback.format_exc()))
	else:
	    sql = "select %s from %s where id='%s'"%(','.join(fields),table,id)
	    try:
		logutil.writelog('db').info("sql: %s"%sql)
		cur.execute(sql)
		result = cur.fetchone()
		user = {}
		for i,k in enumerate(fields):
		    user[k] = result[i]
		return user
	    except:
		logutil.writelog('db').error("Exec: %s,Error: %s"% (sql,traceback.format_exc()))

    def add(table,args):
	sql = 'insert into %s set %s'%(table,','.join(args))
	try:
 	    logutil.writelog('db').info("sql: %s"%sql)
	    cur.execute(sql)
	except:
	    logutil.writelog('db').error("Exec: %s,Error: %s"% (sql,traceback.format_exc()))
	
    def delete(table,id):
	sql = "delete from %s where id='%s'"%(table,id)
	try:
 	    logutil.writelog('db').info("sql: %s"%sql)
	    cur.execute(sql)
	except:
	    logutil.writelog('db').error("Exec: %s,Error: %s"% (sql,traceback.format_exc()))

    def update(table,args,id):
	sql = "update %s set %s where id='%s'"%(table,','.join(args),id)
	try:
 	    logutil.writelog('db').info("sql: %s"%sql)
	    cur.execute(sql)
	except:
	    logutil.writelog('db').error("Exec: %s,Error: %s"% (sql,traceback.format_exc()))
