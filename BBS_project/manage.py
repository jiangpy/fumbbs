#! /usr/bin/env python
# coding:utf-8
from exts import db
from BBS_project import app
from flask_migrate import MigrateCommand,Migrate
from flask_script import Manager
from models import cmsmodels
from models import frontmodels
from models import commonmodels
CMSRole = cmsmodels.CMSRole
CMSUser = cmsmodels.CMSUser
CMSPermission = cmsmodels.CMSPermission
Frontuser = frontmodels.FrontUser
Boards = commonmodels.BoardModel
ElitePostModel = commonmodels.ElitePostModel
PostModel = commonmodels.PostModel
migrate = Migrate(app,db)
manager = Manager(app)

manager.add_command('db',MigrateCommand)


# 添加CMS用户
# @manager.option('-e','--email',dest='email')
# @manager.option('-u','--username',dest='username')
# @manager.option('-p','--password',dest='password')
# def create_cms_user(email,username,password):
#     user = CMSUser.query.filter_by(email=email).first()
#     if user:
#         print u'该邮箱已经注册！不能重复注册！'
#         return
#     else:
#         user = CMSUser(email=email,username=username,password=password)
#         db.session.add(user)
#         db.session.commit()
#         print u'恭喜！CMS用户添加成功！'



# 添加权限组（角色）
@manager.option('-n','--name',dest='name')
@manager.option('-d','--desc',dest='desc')
@manager.option('-p','--permissions',dest='permissions')
def create_role(name,desc,permissions):
    role = CMSRole(name=name.decode('gbk').encode('utf8'),desc=desc.decode('gbk').encode('utf8'),permissions=permissions.decode('gbk').encode('utf8'))
    db.session.add(role)
    db.session.commit()
    print u'权限组（角色）添加成功！'

# CMS用户添加
@manager.option('-e','--email',dest='email')
@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
@manager.option('-r','--rolename',dest='rolename')
def create_cms_user(email,username,password,rolename):
    roleModel = CMSRole.query.filter_by(name=rolename.decode('gbk').encode('utf8')).first()
    if not roleModel:
        print u'该权限组（角色）不存在'
        return
    else:
        cmsuser = CMSUser.query.filter_by(email=email).first()
        if cmsuser:
            print u'该邮箱已经注册不能再次注册！'
            return
        user =CMSUser(username=username,password=password,email=email)
        roleModel.users.append(user)
        db.session.commit()
        print u'用户添加成功!'

@manager.command
def test():
    post = PostModel.query.filter_by(id=118).first()
    quality = ElitePostModel()
    quality.create_user = CMSUser.query.first()
    post.is_elite = quality
    db.session.commit()
@manager.command
def test_permission():
    user = CMSUser.query.filter_by(email='1562873909@qq.com').first()
    print user.permission()



if __name__ == '__main__':
    manager.run()