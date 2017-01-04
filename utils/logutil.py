# coding:utf-8

import logging
import logging.handlers

def writelog(log_name):
    log_file = '/tmp/mysql.log'
    log_level = logging.DEBUG

    # 定义日志格式
    log_format = logging.Formatter('%(asctime)s %(filename)s [line:%(lineno)2d]-%(funcName)s  %(levelname)s %(message)s')
#    fh = logging.FileHandler(log_file)
    fh = logging.handlers.RotatingFileHandler(log_file,mode='a',maxBytes=1024*1024*10,backupCount=5)
    fh.setFormatter(log_format)

    # 实例化日志对象
    logger = logging.getLogger(log_name)
    logger.setLevel(log_level)

    # 每调用一次就会添加一个logger.handler，每次就额外多打印一次日志，if判断使其只调用一次
    if not logger.handlers:
	logger.addHandler(fh)

#    logger.handlers.pop()
    return logger
