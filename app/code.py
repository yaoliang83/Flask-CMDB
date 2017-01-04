#!/usr/bin/python
#coding:utf-8

from flask import render_template,request,redirect,session
from . import app
from config import *
from utils import login_request
from werkzeug import secure_filename
import paramiko
import json,os,sys,re,time
import db
import pysvn
import zipfile

reload(sys)
sys.setdefaultencoding('utf-8')

app.config.from_object(RemoteHost)
app.config.from_object(Table)
app.config.from_object(ProUrl)
fields_code = app.config.get('FIELDS_CODE')
url = app.config.get('URL') # 字典格式
path = '/data/'
hosts = []
allfile = []

for i in app.config:
    if re.findall('HOST.',i):
        hosts.append(app.config.get(i))
    # hosts格式为[['192.168.1.100', 22, 'root', '123456'],['192.168.1.101', 22, 'root', '123456'],['192.168.1.102', 22, 'root', '123456']]

def get_login(realm,username,may_save):
    return True,'test','123456',True

def svncheckout(url,where):
    client = pysvn.Client()
    client.callback_get_login = get_login
    try:
        client.checkout(url,where)
    except Exception,e:
        print 'Error: {}'.format(e)

# 遍历目录中的所有文件
#def dirlist(where):  
#    filelist =  os.listdir(where)  
#  
#    for filename in filelist:  
#        filepath = os.path.join(where, filename)  
#        if os.path.isdir(filepath):  
#            dirlist(filepath)  
#        else:  
#            allfile.append(filepath)  
#    return allfile

def trans(where,filename,host):
    # 文件传输
    tus = (host[0],host[1])
    t = paramiko.Transport(tus)
    t.connect(username=host[2],password=host[3])
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp.put(where,filename)
    t.close()
	   
def exec_comm(comm,host):
    ssh = paramiko.SSHClient()
    #comm = '/root/update.sh '+where

    # 执行远程命令
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host[0],host[1],host[2],host[3],timeout=10)
    stdin,stdout,stderr = ssh.exec_command(comm)
    ssh.close()

def zip_dir(dirname,zipfilename):
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else :
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))
         
    zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
    for tar in filelist:
        arcname = tar[len(dirname):]
        #print arcname
        zf.write(tar,arcname)
    zf.close()

@app.route('/code/',methods=['GET','POST'])
@login_request.login_request
def code():
    role = session.get('role')
    if request.method=='GET':
	return render_template('/code/code.html',role=role)
    else:
	data = dict((k,v[0]) for k,v in dict(request.form).items()) # message, key, project
	print data
	key = data.pop('key')
	project = data['project']
	data['update_persion'] = session.get('name')
	conditions = [ "%s='%s'" %  (k,v) for k,v in data.items()]
	if key == 'mmnn88' and data['project']:
	    try:
		localtime = time.strftime('-%Y-%m-%d-%H:%M:%S')
	        project_name = project+localtime # 例如: 'ecg-2016-12-07-10:00:37'
		zip_name = project_name+'.zip'
		print zip_name
	        svncheckout(url[project],path+project_name) # co 到 '/data/ecg-2016-12-07-10:00:37'
		os.chdir(path) # cd '/data'
	  	zip_dir(project_name,zip_name)
		for host in hosts:
		    trans(zip_name,path+zip_name,host)
		    exec_comm('/bin/bash /root/update.sh '+zip_name,host)
    		db.add('code',conditions)
    		return json.dumps({'code':0,'result':'更新成功'})
	    except Exception, e:
		errmsg = '失败信息 error: '+str(e)
    		return json.dumps({'code':1,'errmsg':errmsg})
	elif not data['project']:
	    return json.dumps({'code':1,'errmsg':errmsg})
	else:
	    errmsg = '许可码无效!'
	    return json.dumps({'code':1,'errmsg':errmsg})

@app.route('/codelist/')
@login_request.login_request
def codelist():
    role = session.get('role')
    codes = db.list('code',fields_code)
    return render_template("/code/codelist.html",codes = codes,role = role)
