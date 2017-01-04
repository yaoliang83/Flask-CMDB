# coding:utf-8
from smtplib import SMTP


def myMail(from_email,passwd,to_email,content):
    SMTPSVR = SMTP('smtp.yeah.net')
#    SMTPSVR = SMTP('smtp.sina.com')

    body = '''\From: {}\r\nTo: {}\r\nSubject: 'JOB EMAIL'\r\n\r\n操作结果: {}\r\n'''.format(from_email,to_email,content)

    sendSvr = SMTPSVR
    sendSvr.login(from_email,passwd)
    errs = sendSvr.sendmail(from_email,[to_email],body)
    sendSvr.quit()

