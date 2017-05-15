#! /usr/bin/env python
# coding:utf-8

from flask import Blueprint,url_for
from exts import db
import flask
from utils.captcha.mycaptcha import Captcha
from forms.frontforms import GetSmsCaptchaForm,UserRegistForm,UserLoginForm,PersonageSettingForm,FrontForgetPassword,Get_Forgetpwd_CaptchaForm
from models.frontmodels import FrontUser
from utils import my_sms_captcha,create_captcha,myjson,mycache
from decorators.frontdecorators import login_required
import constants
from tasks import celery_send_phonecaptcha
from datetime import datetime
try:
    from StringIO import StringIO
except:
    from io import BytesIO as StringIO

bp = Blueprint('account',__name__,url_prefix='/account')

# 用户注册
@bp.route('/regist/',methods=['GET','POST'])
def regist():
    if flask.request.method == 'GET':
        message = ''
        return flask.render_template('front/front_regist.html',message=message)
    else:
        form = UserRegistForm(flask.request.form)
        if form.validate():
            telephone = form.telephone.data
            username = form.username.data
            password = form.password.data
            user = FrontUser(telephone=telephone,username=username,password=password)
            db.session.add(user)
            db.session.commit()
            return flask.redirect(url_for('front.index'))
        else:
            telephone = form.telephone.data
            username = form.username.data
            tel_captcha = form.tel_captcha.data
            graph_captcha = form.graph_captcha.data
            error = form.get_error()
            return flask.render_template('front/front_regist.html',message=error,telephone=telephone,username=username,tel_captcha=tel_captcha)

# 用户注册短信验证码发送
@bp.route('/sms_captcha/', methods=['post'])
def sms_captcha():
    form = GetSmsCaptchaForm(flask.request.form)
    if form.validate():
        telephone = form.telephone.data
        captcha = create_captcha.number_captcha()
        if mycache.get(telephone):
            mycache.delete(telephone)
            return myjson.json_params_error('已经向该手机号码发送过验证码了，请查收！')
        # 调用封装好的短信验证码发送
        # 使用celery异步发送验证码
        celery_send_phonecaptcha(sms_free_sign_name=constants.SMS_FREE_sign_NAME, rec_num=telephone,
                                 sms_param=captcha, sms_temaplate_code=constants.SMS_TEMAPLATE_CODE)
        # 设置验证码到缓存中
        mycache.set(telephone, captcha, 60 * 15)
        return myjson.json_result()
    else:
        error = form.get_error()
        return myjson.json_params_error(message=error)


# 用户登录
@bp.route('/login/',methods=['GET','POST'])
def login():
    if flask.request.method == 'GET':
        return flask.render_template('front/front_login.html',error='')
    else:
        form = UserLoginForm(flask.request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password.data
            remember = form.remember.data
            print remember
            user = FrontUser.query.filter_by(telephone=telephone).first()
            if user and user.check_password(password):
                flask.session[constants.FRONT_SESSION_ID] = user.uid
                if remember:
                    flask.session.permanent = True
                else:
                    flask.session.permanent = False
                if user.now_login_time:
                    if user.last_login_time.day != user.now_login_time.day:
                        user.points += 2
                        user.last_login_time = user.now_login_time
                        user.now_login_time = datetime.now()
                        db.session.commit()
                else:
                    user.now_login_time = datetime.now()
                    user.last_login_time = user.now_login_time
                    db.session.commit()
                next = flask.request.args.get('next')
                if next:
                    return flask.redirect(next)
                else:
                    return flask.redirect(url_for('front.index'))
            else:
                return flask.render_template('front/front_login.html', error=form.get_error(), telephone=telephone)

        else:
            telephone = form.telephone.data
            return flask.render_template('front/front_login.html',error=form.get_error(),telephone=telephone)

# 密码修改手机验证码发送
@bp.route('/get_telephone_captcha/',methods=['POST'])
def get_telephone_captcha():
    form = Get_Forgetpwd_CaptchaForm(flask.request.form)
    if form.validate():
        telephone = form.telephone.data
        print telephone
        captcha = create_captcha.create_captcha()
        # 使用celery异步发送验证码
        celery_send_phonecaptcha(sms_free_sign_name=constants.SMS_FREE_sign_NAME, rec_num=telephone,sms_param=captcha, sms_temaplate_code=constants.SMS_TEMAPLATE_CODE_CHANGE)
        # 设置验证码到缓存中
        mycache.set(telephone, captcha, 60 * 15)
        return myjson.json_result()
    else:
        return myjson.json_params_error(message=form.get_error())




# 密码修改
@bp.route('/forget_password/',methods=['GET','POST'])
def forget_password():
    if flask.request.method == 'GET':
        return flask.render_template('front/front_forget_password.html')
    else:
        form = FrontForgetPassword(flask.request.form)
        if form.validate():
            telephone = form.telephone.data
            new_password = form.new_password.data
            user = FrontUser.query.filter_by(telephone=telephone).first()
            user.password = new_password
            db.session.commit()
            return myjson.json_result()
        else:
            return myjson.json_params_error(form.get_error())



#  退出登录
@bp.route('/logout/')
@login_required
def logout():
    flask.session.pop(constants.FRONT_SESSION_ID)
    return flask.redirect(flask.url_for('front.index'))




# 个人设置
@bp.route("/personagesetting/<string:user_id>/",methods=['GET','POST'])
@login_required
def personagesetting(user_id):
    if flask.request.method == 'GET':
        return flask.render_template('front/personagesettings.html')
    else:
        form = PersonageSettingForm(flask.request.form)
        if form.validate():
            username = form.username.data
            realname = form.realname.data
            avater = form.avater.data
            qq = form.qq.data
            signature = form.signature.data
            uid = form.user_id.data
            gender = form.gender.data
            if uid != user_id:
                return myjson.json_params_error(u'当前用户不存在！')
            userModel = FrontUser.query.filter_by(uid=user_id).first()
            if userModel.username != username:
                userModel.username = username

            if userModel.realname != realname:
                userModel.realname = realname

            if userModel.avater != avater:
                userModel.avater = avater

            if userModel.qq != qq:
                userModel.qq = qq

            if userModel.signature != signature:
                userModel.signature = signature

            if userModel.gender != gender:
                userModel.gender = gender
            db.session.commit()
            return myjson.json_result()
        else:
            return myjson.json_params_error(form.get_error())

# 修改邮箱
@bp.route('/update_email/',methods=['GET','POST'])
def update_email():
    if flask.request.method == 'GET':
        return flask.render_template('front/update_email.html')


# 用户详情页
@bp.route('/profile/<string:user_id>',methods=['GET'])
def user_profile(user_id):
    if not user_id:
        return flask.abort(404)
    user = FrontUser.query.get(user_id)
    if user:
        context={
            'current_user':user
        }
        return flask.render_template('front/front_profile.html',**context)
    else:
        return flask.abort(404)

@bp.route('/profile/posts/',methods=["GET"])
def profile_posts():
    user_id = flask.request.args.get('user_id')
    if not user_id:
        return flask.abort(404)

    user = FrontUser.query.get(user_id)
    print '-' * 20
    print len(user.posts)
    print '-' * 20
    if user:
        context = {
            'current_user': user,
        }
        return flask.render_template('front/front_profile_posts.html', **context)
    else:
        return flask.abort(404)
# 生成图形验证码
@bp.route('/create_captcha/')
def create_graph_captcha():
    text,image = Captcha.gene_code()
    out = StringIO()
    image.save(out,'png')
    out.seek(0)
    response = flask.make_response(out.read())
    response.content_type = 'image/png'
    # 将验证码设置到缓存中
    mycache.set(text.lower(), text.lower())
    return response