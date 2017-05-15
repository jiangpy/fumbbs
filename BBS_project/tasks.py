# coding:utf-8

from celery import Celery
from utils import mymail,my_sms_captcha,create_captcha
from config import CELERY_BROKER_URL,CELERY_RESULT_BACKEND
from exts import app
import constants
import time

# 初始化celery
def make_celery(app):
    celery = Celery(app.import_name, broker=CELERY_BROKER_URL,backend=CELERY_RESULT_BACKEND)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(app)

@celery.task
def celery_send_mail(receivers,subject,body=None,html=None):
    with app.app_context():
        mymail.send_mail(receivers, subject, body, html)


@celery.task
def celery_send_phonecaptcha(sms_free_sign_name, rec_num, sms_temaplate_code, sms_param):
    with app.app_context():
        my_sms_captcha.sms_captcha(sms_free_sign_name, rec_num, sms_temaplate_code, sms_param)