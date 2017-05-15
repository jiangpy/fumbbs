#! /usr/bin/env python
# coding:utf-8
HOST = '127.0.0.1'
USERNANE = 'root'
PASSWORD = '199564'
PORT = 3306
DATABASE = 'bbs'

DB_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8'.format(USERNANE,PASSWORD,HOST,PORT,DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI

SERVER_NAME = 'jbbs.cn'
SQLALCHEMY_TRACK_MODIFICATIONS = False

import os

SECRET_KEY = os.urandom(24)


#发送邮件配置
MAIL_SERVER = 'smtp.163.com'
MAIL_PORT ='465'
MAIL_USERNAME = 'angstrive@163.com'
MAIL_PASSWORD = 'jiang1995zhen'
MAIL_DEFAULT_SENDER = 'angstrive@163.com'
MAIL_USE_SSL = True


# celery 配置
CELERY_BROKER_URL = 'redis://:199564@123.206.29.48:6379/0'
CELERY_RESULT_BACKEND = 'redis://:199564@123.206.29.48:6379/0'