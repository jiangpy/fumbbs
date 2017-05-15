#! /usr/bin/env python
# coding:utf-8
import constants
import flask
from functools import wraps
from utils import myjson
from models.cmsmodels import  CMSPermission
# 登录限制
def login_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        user = flask.session.get(constants.CMS_SESSION_ID)
        if user:
            return func(*args,**kwargs)
        else:
            return flask.redirect(flask.url_for('cms.login'))
    return wrapper

# 权限限制
def permission_required(permission):

    def deco(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            if flask.g.cms_user.has_permission(permission):
                return func(*args,**kwargs)
            else:
                if flask.request.is_xhr:
                    return myjson.json_unauth_error(message=u'对不起，您没有权限访问！')
                else:
                    flask.abort(401)
        return wrapper
    return deco


# 超级管理员权限限制
def superadmin_required(func):
    return permission_required(CMSPermission.ADMINISTRATOR)(func)

