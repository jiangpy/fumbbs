#! /usr/bin/env python
# coding:utf-8

from exts import db
import shortuuid
import datetime
from werkzeug.security import generate_password_hash,check_password_hash

class GenderType(object):
    SECRET = 0
    MAN = 1
    WOMAN = 2

class FrontUser(db.Model):
    __tablename__ = 'front_user'
    uid = db.Column(db.String(100),primary_key=True,default=shortuuid.uuid())
    username = db.Column(db.String(20), nullable=False)
    telephone = db.Column(db.String(11),nullable=False,unique=True)
    _password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=True, unique=True)  # unique 唯一
    join_time = db.Column(db.DateTime, default=datetime.datetime.now)
    is_active = db.Column(db.Boolean, default=True)
    last_login_time = db.Column(db.DateTime, nullable=True)
    now_login_time = db.Column(db.DateTime, nullable=True)
    qq = db.Column(db.String(15))
    realname = db.Column(db.String(20))
    gender = db.Column(db.Integer,default=GenderType.SECRET)
    signature = db.Column(db.String(200))
    points = db.Column(db.Integer,default=0)
    avater = db.Column(db.String(100),default='http://oo78d7e19.bkt.clouddn.com/%E9%BB%98%E8%AE%A4%E5%A4%B4%E5%83%8F.jpg')

    def __init__(self,username, password,telephone):
        self.username = username
        self.password = password
        self.telephone = telephone

    @property
    def password(self):
        return self._password



    @password.setter
    def password(self,rawpwd):
        self._password = generate_password_hash(rawpwd)


    def check_password(self,rawpwd):
        return check_password_hash(self._password,rawpwd)
