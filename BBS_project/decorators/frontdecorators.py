#! /usr/bin/env python
# coding:utf-8
from functools import wraps
from constants import FRONT_SESSION_ID
import flask
# 登录限制
def login_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        next = flask.request.path
        if flask.session.get(FRONT_SESSION_ID):
            return func(*args,**kwargs)
        else:
            return flask.redirect(flask.url_for('account.login',next=next))
    return wrapper