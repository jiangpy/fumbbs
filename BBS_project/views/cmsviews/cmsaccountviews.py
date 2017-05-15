#! /usr/bin/env python
# coding:utf-8

from cms_exts import bp
import flask
from forms.cmsforms import LoginForm,CMSResetpwdForm,GetCaptchaForm,ResetEmailForm,AddCmsUserForm,CMSBlackListForm
from models.cmsmodels import CMSUser,CMSRole
from models.frontmodels import FrontUser
import constants
from utils import myjson,mymail
from decorators.cmsdecorators import login_required,permission_required,superadmin_required
from exts import db
import string
import random
from utils import mycache
from tasks import celery_send_mail


# 登录view
@bp.route('/login/',methods=['GET','POST'])
def login():
    if flask.request.method == 'GET':
        return flask.render_template('cms/cms_login.html')
    else:
        form = LoginForm(flask.request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            print type(remember),remember
            if user and user.check_password(password):
                if user.is_active == False:
                    return myjson.json_unauth_error(message=u'对不起！您没有权限登录')
                flask.session[constants.CMS_SESSION_ID] = user.uid
                if remember == 1:
                    flask.session.permanent = True
                else:
                    flask.session.permanent = False
                return myjson.json_result()
            else:
                return myjson.json_params_error(u'邮箱或密码错误')
        else:
            message = form.get_error()
            return myjson.json_params_error(message=message)


# 退出登录view
@bp.route('/logout/')
@login_required
def logout():
    flask.session.pop(constants.CMS_SESSION_ID)
    return flask.redirect(flask.url_for('cms.login'))




# 个人信息view
@bp.route('/profile/',methods= ['GET'])
@login_required
def profile():
    return flask.render_template('cms/cms_profile.html')

# 修改密码view
@bp.route('/resetpwd/',methods=['GET','POST'])
@login_required
def resetpwd():
    if flask.request.method == 'GET':
        return flask.render_template('cms/cms_resetpwd.html')
    else:
        form = CMSResetpwdForm(flask.request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            newpwdrepeat = form.newpwdrepeat.data

            # 拿到数据库中的用户密码与用户输入的原密码作比较
            if flask.g.cms_user.check_password(oldpwd):
                flask.g.cms_user.password = newpwd
                db.session.commit()
                return myjson.json_result(message=u'密码修改成功！')
            else:
                return myjson.json_params_error(u'密码输入错误！')
        else:
            message = form.get_error()
            return myjson.json_params_error(message=message)

# 邮箱修改
@bp.route('/resetemail/',methods=['GET','POST'])
@login_required
def resetemail():
    if flask.request.method == 'GET':
        return flask.render_template('cms/resetemail.html')
    else:
        form = ResetEmailForm(flask.request.form)
        if form.validate():
            newemail = form.newemail.data
            if flask.g.cms_user.email == newemail:
                return myjson.json_params_error(message=u'两个邮箱一致！无需更改！')
            flask.g.cms_user.email = newemail
            db.session.commit()
            return myjson.json_result()
        else:
            error = form.get_error()
            return myjson.json_params_error(error)

# 邮件发送接口
@bp.route('/mail_captcha/',methods=['POST'])
@login_required
def mail_captcha():
    form = GetCaptchaForm(flask.request.form)
    if form.validate():
        email = form.oldemail.data
        if mycache.get(email):
            return myjson.json_params_error(u'已经向该邮箱发送完验证码！请2分钟之后再试！')
        source = list(string.letters + string.digits)
        captcha = ''.join(random.sample(source,5))

        celery_send_mail.delay(subject=u'Python论坛邮箱验证码',receivers=email,body=u'邮箱验证码为：'+captcha)
        return myjson.json_result()
        # if mymail.send_mail(subject=u'Python论坛邮箱验证码',receivers=email,body=u'邮箱验证码为：'+captcha):
        #     mycache.set(email,captcha,60*2)
        #     return myjson.json_result()
        # else:
        #     return myjson.json_server_error(u'邮件发送失败，请重试！')
    else:
        error = form.get_error()
        return myjson.json_params_error(error)

# CMS用户管理页面
@bp.route('/cmsusermanage/')
@login_required
@superadmin_required
def cmsusermanage():
    cmsusers = CMSUser.query.all()
    return flask.render_template('cms/cmsusermanage.html',cmsusers=cmsusers)


# 添加CMS管理员
@bp.route('/cmsusermanage/adduser/',methods=['GET','POST'])
@login_required
@superadmin_required
def adduser():
    if flask.request.method == 'GET':
        roles = CMSRole.query.all()
        return flask.render_template('cms/add_cmssuer.html',roles=roles)
    else:
        form = AddCmsUserForm(flask.request.form)
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            roles = flask.request.form.getlist('roles[]')
            if not roles:
                return myjson.json_params_error(message=u'至少要给一个权限')
            userModel = CMSUser.query.filter_by(email=email).first()
            if userModel:
                return myjson.json_params_error(message=u'该邮箱已存在，不能重复添加！')
            user = CMSUser(username=username,email=email,password=password)
            for role_id in roles:
                role = CMSRole.query.get(role_id)
                role.users.append(user)
            db.session.commit()
            return myjson.json_result()
        else:
            error = form.get_error()
            return myjson.json_params_error(message=error)


# 编辑CMS管理员
@bp.route('/cmsusermanage/edit_cmsuser/',methods=['GET','POST'])
@login_required
@superadmin_required
def edit_cmsuser():
    uid = flask.request.args.get('cmsuser')
    if flask.request.method=='GET':
        cmsuser = CMSUser.query.get(uid)
        roles = CMSRole.query.all()
        current_roles = [role.id for role in cmsuser.roles]
        content = {
            'cmsuser':cmsuser,
            'roles':roles,
            # current_roles表示当前用户所有权限id列表
            'current_roles':current_roles,
        }
        if not cmsuser:
            flask.abort(404)
        return flask.render_template('cms/edit_cmsuser.html',**content)
    else:
        user_id = flask.request.form.get('user_id')
        user = flask.request.args.get('cmsuser')
        roles = flask.request.form.getlist('roles[]')
        if not user_id:
            return myjson.json_params_error(message=u'用户不存在')
        if not roles:
            return myjson.json_params_error(message=u'必须选择一个权限')
        if user_id == flask.g.cms_user.uid:
            return myjson.json_params_error(message=u'不能自己操作自己！')
        user = CMSUser.query.get(user_id)
        # 清除该用户以前的权限
        user.roles[:] = []
        for role_id in roles:
            roleModel = CMSRole.query.get(role_id)
            user.roles.append(roleModel)
            db.session.commit()
            return myjson.json_result()

# CMS用户加入与移出黑名单
@bp.route('/black_list/',methods=['POST'])
@login_required
@superadmin_required
def black_list():
    form = CMSBlackListForm(flask.request.form)
    if form.validate():
        user_id = form.user_id.data
        is_active = form.is_active.data
        if not user_id:
            return myjson.json_params_error(message=u'没有该用户')
        if user_id == flask.g.cms_user.uid:
            return myjson.json_params_error(message=u'不能自己操作自己！')
        user = CMSUser.query.get(user_id)
        # 如果 is_active == 1 ,user.is_active=False否者user.is_active=True
        user.is_active = False if is_active == 1 else True
        db.session.commit()
        return myjson.json_result()
    else:
        error = form.get_error()
        return myjson.json_params_error(message=error)


# 前台用户管理操作
@bp.route('/frontuser_manage/',methods=['GET','POST'])
@login_required
def frontuser_manage():
    if flask.request.method == 'GET':
        """
            currentsort = '1' 按注册时间排序（默认时间排序）
            currentsort = '2' 按评论量排序
            currentsort = '3' 按发帖量排序
        """
        currentsort = flask.request.args.get('sort')
        print currentsort
        if not currentsort or currentsort == '1':
            users = FrontUser.query.order_by(FrontUser.join_time.desc()).all()
        if currentsort == '2':
            users = FrontUser.query.all()
        if currentsort == '3':
            users = FrontUser.query.all()
        context = {
            'frontusers':users,
            'currentsort':currentsort
        }
        return flask.render_template('cms/cms_frontuser_manage.html', **context)
    else:
        uid = flask.request.form.get('uid')
        is_active = int(flask.request.form.get('is_active'))
        user = FrontUser.query.get(uid)
        if is_active == 1:
            user.is_active = False
        else:
            user.is_active = True
        db.session.commit()
        return myjson.json_result()


# 查看前台用户详情
@bp.route('/frontuser_manage/userdetail/')
@login_required
def front_user_detail():
    uid = flask.request.args.get('userid')
    user = FrontUser.query.get(uid)
    context = {
        'frontuser':user,
    }
    return flask.render_template('cms/cms_frontuser_detail.html',**context)
# 设置当前登录的cms用户为全局变量
@bp.context_processor
def cms_context_processor():
    uid = flask.session.get(constants.CMS_SESSION_ID)
    if uid:
        user = CMSUser.query.get(uid)
        return {'cms_user':user}
    else:
        return {}


# 将当前登陆的cms用户添加到 g 对象上去
@bp.before_request
def cms_before_requset():
    uid = flask.session.get(constants.CMS_SESSION_ID)
    if uid:
        user = CMSUser.query.get(uid)
        flask.g.cms_user = user

@bp.errorhandler(404)
def cms_not_found(error):
    return flask.render_template('common/404.html')

@bp.errorhandler(401)
def cms_not_found(error):
    return flask.render_template('common/401.html')