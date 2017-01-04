# coding:utf-8
# flask-mail插件

from app import app
from flask_mail import Mail,Message
from threading import Thread

mail = Mail(app)

def send_async_email(app,msg):
    with app.app_content():
	mail.send(msg)

#@app.route('newMail')
def newMail(from_user,passwd,to_user,content):
    app.config['MAIL_SERVER'] = 'smtp.qq.com'
    app.config['MAIL_PORT'] = 25
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = from_user
    app.config['MAIL_PASSWORD'] = passwd

    msg = Message('job email',sender=from_user,recipients=[to_user])
    msg.html = '<b>'+content+'</b>'
    print msg.html
    mail.send(msg)

  #  thr = Thread(target=send_async_email,args=[app,msg])
  #  thr.start()
