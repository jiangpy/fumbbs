#! /usr/bin/env python
# coding:utf-8

from wtforms import StringField,BooleanField,ValidationError,IntegerField
from wtforms.validators import InputRequired,Length,Email,EqualTo
from baseform import BaseForm
from models.cmsmodels import CMSUser
from utils import mycache


# 登录验证
class LoginForm(BaseForm):
    email = StringField(validators=[Email(u'邮箱格式不正确'),InputRequired(message=u'邮箱不能为空')])
    password = StringField(validators=[Length(6,20,message=u'密码必须在6-20位字符之间'),InputRequired(u'密码不能为空')])
    remember = IntegerField()

# 修改密码验证
class CMSResetpwdForm(BaseForm):
    oldpwd = StringField(validators=[InputRequired(message=u'请输入原密码！')])
    newpwd = StringField(validators=[InputRequired(message=u'请输入需要修改的密码！'),Length(6,20,message='密码长度必须在6-20位之间')])
    newpwdrepeat = StringField(validators=[EqualTo('newpwd',message=u'两次密码不一致！')])


# 获取邮箱验证码验证
class GetCaptchaForm(BaseForm):
    oldemail = StringField(validators=[InputRequired(message=u'请输入邮箱'), Email(message=u'请正确输入邮箱')])

    def validate_oldemail(self,field):
        oldemail = self.oldemail.data
        user = CMSUser.query.filter_by(email=oldemail).first()
        if user:
            return True
        else:
            raise ValidationError(u'输入的不是当前登录的邮箱')

# 修改邮箱验证码
class ResetEmailForm(BaseForm):
    oldemail = StringField(validators=[InputRequired(message=u'请输入邮箱'), Email(message=u'请正确输入邮箱')])
    captcha = StringField(validators=[InputRequired(message=u'必须输入验证码')])
    newemail = StringField(validators=[InputRequired(message=u'请输入需要修改的邮箱'),Email(u'请输入正确的邮箱')])
    def validate_captcha(self,field):
        email = self.oldemail.data
        captcha = field.data
        captcha_cache = mycache.get(email)
        print captcha
        print captcha_cache
        if captcha_cache and captcha.lower() == captcha_cache.lower():
            return True
        else:
            raise ValidationError('验证码错误！')

# 添加管理员验证
class AddCmsUserForm(BaseForm):
    username = StringField(validators=[InputRequired(message=u'用户名不能为空'),Length(3,10,message=u'用户名长度只能在5-50字符之间')])
    email = StringField(validators=[Email(u'邮箱格式不正确'),InputRequired(message=u'邮箱不能为空')])
    password = StringField(validators=[InputRequired(message=u'密码不能为空'),Length(6,20,message=u'密码长度只能在6-20字符之间')])


#  CMS用户黑名单验证
class CMSBlackListForm(BaseForm):
    user_id = StringField(validators=[InputRequired(message=u'没有该用户')])
    is_active = IntegerField(validators=[InputRequired(message=u'必须选择是加入黑名单还是移出黑名单')])



