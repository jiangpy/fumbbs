#! /usr/bin/env python
# coding:utf-8
from baseform import BaseForm,Graph_CaptchaForm
from wtforms import StringField,IntegerField,ValidationError,BooleanField
from wtforms.validators import InputRequired,EqualTo,Length,URL,Email
import re
from utils import myjson,mycache
from models.frontmodels import FrontUser




# 前台用户发送验证码的手机号码验证
class GetSmsCaptchaForm(BaseForm):
    telephone = StringField(validators=[InputRequired(message=u'没有填写手机号码'),Length(11,11,message=u'不是正确的11位手机号码！')])
    def validate_telephone(self,filed):
        telephone=self.telephone.data
        telephone_re = re.compile('^1(3[0-9]|4[57]|5[0-35-9]|7[0135678]|8[0-9])\\d{8}$')
        telephonematch = telephone_re.match(telephone)
        if not telephonematch:
            raise ValidationError(u'不是正确的11位手机号码！')
        telephone_data = FrontUser.query.filter_by(telephone=telephone).first()
        if telephone_data:
            raise ValidationError(message=u'该手机号码已经注册！不能重复注册！')

# 前台用户注册验证
class UserRegistForm(BaseForm,Graph_CaptchaForm):
    telephone = StringField()
    tel_captcha = StringField(validators=[InputRequired(message=u'请填写验证码')])
    username = StringField(validators=[InputRequired(message=u'请输入用户名'),Length(5,15,message=u'用户名长度只能为5-15位字母和数字')])
    password = StringField(validators=[Length(6, 20, message=u'密码必须在6-20位字符之间'), InputRequired(u'密码不能为空')])
    password_repeat = StringField(validators=[EqualTo('password',message=u'两次密码不相同！')])

    def validate_telephone(self,filed):
        telephone = filed.data
        telephone_data = FrontUser.query.filter_by(telephone=telephone).first()
        if telephone_data:
            raise ValidationError(message=u'该手机号码已经注册！不能重复注册！')

    def validate_tel_captcha(self,filed):
        tel_captcha = filed.data
        telephone= self.telephone.data
        cacha_captcha = mycache.get(telephone)
        if tel_captcha != cacha_captcha or not cacha_captcha:
            raise ValidationError(message=u'短信验证码错误！')
        else:
            return True



# 前台用户登录验证
class UserLoginForm(BaseForm,Graph_CaptchaForm):
    telephone = StringField(validators=[InputRequired(message=u'没有填写手机号码'), Length(11, 11, message=u'不是正确的11位手机号码！')])
    password = StringField(validators=[Length(6, 20, message=u'密码必须在6-20位字符之间'), InputRequired(u'密码不能为空')])
    graph_captcha = StringField(validators=[Length(4,4,message=u'验证码错误'),InputRequired(message=u'请输入验证码')])
    remember = IntegerField()

    def validate_telephone(self,filed):
        telephone = filed.data
        password = self.password.data
        print password
        user = FrontUser.query.filter_by(telephone=telephone).first()
        if not user:
            raise ValidationError(message=u'该手机号没有注册！')
        else:
            if user.check_password(password):
                return True
            else:
                raise ValidationError(message=u'手机号码或密码错误！')

# 忘记密码，密码修改验证
class FrontForgetPassword(BaseForm):
    telephone = StringField(validators=[InputRequired(message=u'没有填写手机号码'), Length(11, 11, message=u'不是正确的11位手机号码！')])
    new_password = StringField(validators=[InputRequired(message=u'请输入新密码'),Length(6, 20, message=u'密码必须在6-20位字符之间')])
    tel_captcha = StringField(validators=[InputRequired(message=u'请输入验证码'),Length(4,4,message=u'验证码错误！')])
    repe_new_password = StringField(validators=[EqualTo('new_password',message=u'两次密码不一致！')])

    def validate_tel_captcha(self, filed):
        tel_captcha = filed.data
        telephone = self.telephone.data
        cacha_captcha = mycache.get(telephone)
        if tel_captcha.lower() != cacha_captcha.lower() or not cacha_captcha:
            raise ValidationError(message=u'验证码错误！')
        else:
            return True

    def validate_telephone(self,filed):
        telephone = filed.data
        print telephone
        telephone_re = re.compile('^1(3[0-9]|4[57]|5[0-35-9]|7[0135678]|8[0-9])\\d{8}$')
        telephonematch = telephone_re.match(telephone)
        if not telephonematch:
            raise ValidationError(u'不是正确的11位手机号码！')
        user = FrontUser.query.filter_by(telephone=telephone).first()
        if not user:
            raise ValidationError(message=u'该手机号码并未注册！')
        else:
            return True


# 密码修改手机验证码发送验证
class Get_Forgetpwd_CaptchaForm(BaseForm):
    telephone = StringField(validators=[InputRequired(message=u'没有填写手机号码'), Length(11, 11, message=u'不是正确的11位手机号码！')])

    def validate_telephone(self, filed):
        telephone = filed.data
        print telephone
        telephone_re = re.compile('^1(3[0-9]|4[57]|5[0-35-9]|7[0135678]|8[0-9])\\d{8}$')
        telephonematch = telephone_re.match(telephone)
        if not telephonematch:
            raise ValidationError(u'不是正确的11位手机号码！')
        user = FrontUser.query.filter_by(telephone=telephone).first()
        if not user:
            raise ValidationError(message=u'该手机号码并未注册！')
        else:
            return True





#  个人设置信息验证
class PersonageSettingForm(BaseForm):
    username = StringField(validators=[Length(5, 15, message=u'用户名长度只能为5-15位字母和数字'),InputRequired(message=u'请输入用户名') ])
    realname = StringField()
    avater = StringField(validators=[URL(u'头像链接格式不正确！')])
    qq = StringField()
    signature = StringField()
    user_id = StringField(validators=[InputRequired(message=u'当前用户不存在！')])
    gender  = IntegerField(validators=[InputRequired(message=u'请选择显示的性别')])