#! /usr/bin/env python
# coding:utf-8
from exts import db
import uuid
import datetime
from werkzeug.security import generate_password_hash,check_password_hash

# 权限设置
class CMSPermission(object):
    # 超级管理员
    ADMINISTRATOR = 255
    # 普通管理员
    OPERATOR = 1
    PERMISSION_MAP = {
        ADMINISTRATOR:(u'超级管理员',u'拥有CMS系统全部操作权限'),
        OPERATOR:(u'普通管理员',u'只拥有管理帖子与前端用户操作权限')
    }


# CMS用户与角色的中间表
cms_user_role = db.Table('cms_user_role',
    db.Column('role_id',db.Integer,db.ForeignKey('cms_role.id'),primary_key=True),
    db.Column('user_id',db.String(100),db.ForeignKey('cmsuser.uid'),primary_key=True)
                         )


# 权限组（角色组）
class CMSRole(db.Model):
    __tablename__ = 'cms_role'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True   )
    name = db.Column(db.String(100),nullable=False)
    desc = db.Column(db.String(200),nullable=True)
    create_tine = db.Column(db.DateTime,default= datetime.datetime.now)
    permissions = db.Column(db.Integer,nullable=False,default=CMSPermission.OPERATOR)

class CMSUser(db.Model):
    __tablename__ = 'cmsuser'

    uid = db.Column(db.String(100),primary_key=True,default=uuid.uuid4())
    username = db.Column(db.String(100),nullable=False)
    _password = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(100),nullable=False,unique=True) #unique 唯一
    join_time = db.Column(db.DateTime,default=datetime.datetime.now)
    is_active = db.Column(db.Boolean,default=True)
    last_login_time =db.Column(db.DateTime,nullable=True)

    roles = db.relationship('CMSRole',secondary=cms_user_role,backref='users')
    # 修改构造函数实现密码加密
    def __init__(self,username,password,email):
        self.username = username
        self.email = email
        self.password = password

    @property #将一个方法变为属性
    def password(self):
        return self._password


    @password.setter
    def password(self,rawpwd):
        self._password = generate_password_hash(rawpwd)


    def check_password(self,rawpwd):
        return check_password_hash(self.password,rawpwd)


    def has_permission(self,permission):
        if not self.roles:
            return False
        all_permission  = 0
        for role in self.roles:
            all_permission = all_permission | role.permissions
        if all_permission & permission == permission:
            return True
        else:
            return False

    @property
    def is_superadmin(self):
        return self.has_permission(CMSPermission.ADMINISTRATOR)


    @property
    def permissions(self):
        if not self.roles:
            return None
        all_permissions = 0
        for role in self.roles:
            all_permissions |= role.permissions
        for permission,desc in CMSPermission.PERMISSION_MAP.iteritems():
            if permission & all_permissions ==permission:
                permission_dicts = []
                permission_dicts.append({permission:desc})
        return permission_dicts