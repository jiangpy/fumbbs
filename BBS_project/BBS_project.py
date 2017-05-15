# coding:utf-8
from flask import Flask
import flask
from flask_wtf import CSRFProtect
from exts import db,mail
import config
from views.cmsviews import cmsaccountviews,cmspostviews
from views.frontviews import frontaccountviews,frontpostviews
from constants import FRONT_SESSION_ID
from models.frontmodels import FrontUser
from datetime import datetime
from exts import app


app.register_blueprint(cmspostviews.bp)
app.register_blueprint(cmsaccountviews.bp)
app.register_blueprint(frontpostviews.bp)
app.register_blueprint(frontaccountviews.bp)

CSRFProtect(app)



@app.before_request
def post_before_request():
    uid = flask.session.get(FRONT_SESSION_ID)
    if uid:
        user = FrontUser.query.get(uid)
        flask.g.front_user = user



@app.context_processor
def post_cintext_processor():
    uid = flask.session.get(FRONT_SESSION_ID)
    if uid:
        user = flask.g.front_user
        return {'front_user':user}
    return {}





@app.template_filter('filter_time')
def timefilter(h_time):
    if type(h_time) is datetime:
        nowtime = datetime.now()
        time_difce = (nowtime-h_time).total_seconds()
        if time_difce < 60:
            return u'刚刚'
        elif time_difce >60 and time_difce <=60*60:
            tmptime = time_difce / 60
            return  u'%s分钟之前' %int(tmptime)
        elif 60*60*24 > time_difce > 60*60:
            tmptime = time_difce / (60*60)
            return u'%s小时之前' %int(tmptime)
        elif 60*60*24*30 > time_difce > 60*60*24:
            tmptime = time_difce/ (60*60*24)
            return u'%s天之前' %int(tmptime)
        elif nowtime.year == h_time.year:
            return h_time.strftime('%m-%d %H:%M:%S')
        else:
            return h_time.strftime('%Y-%m-%d %H:%M:%S')
    return h_time

if __name__ == '__main__':
    app.run(debug=True, port=80)
