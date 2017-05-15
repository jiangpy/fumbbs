#! /usr/bin/env python
# coding:utf-8

from flask_wtf import FlaskForm
from utils import mycache
from wtforms import ValidationError,StringField
from wtforms.validators import InputRequired,Length
import re

class BaseForm(FlaskForm):
    def get_error(self):
        _,values = self.errors.popitem()
        message = values[0]
        return message


class Graph_CaptchaForm(object):
    graph_captcha = StringField(validators=[InputRequired(message=u'请输入验证码！')])
    def validate_graph_captcha(self,filed):
        graph_captcha = self.graph_captcha.data
        print 'graph_captcha:',graph_captcha
        cacha_captcha = mycache.get(graph_captcha)
        if not cacha_captcha or cacha_captcha.lower() != graph_captcha.lower():
            raise ValidationError(message=u'图形验证码错误！')
        else:
            return True

# class GetTelephoneCaptchaForm(object):
#     telephone = StringField(validators=[InputRequired(message=u'没有填写手机号码'), Length(11, 11, message=u'不是正确的11位手机号码！')])
#
#     def validate_telephone(self,filed):
#         telephone=self.telephone.data
#         telephone_re = re.compile('^1(3[0-9]|4[57]|5[0-35-9]|7[0135678]|8[0-9])\\d{8}$')
#         telephonematch = telephone_re.match(telephone)
#         if not telephonematch:
#             raise ValidationError(u'不是正确的11位手机号码！')
#         else:
#             return True