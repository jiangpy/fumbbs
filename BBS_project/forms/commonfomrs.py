#! /usr/bin/env python
# coding:utf-8
from baseform import BaseForm,Graph_CaptchaForm
from wtforms import StringField,BooleanField,ValidationError,IntegerField,TextField
from wtforms.validators import InputRequired,Length,Email,EqualTo

# 添加板块
class AddBoardForm(BaseForm):
    name = StringField(validators=[InputRequired(message=u'请输入版块名称'),Length(2,10,message=u'版块名称只能为2-10位')])

# 编辑板块
class EditBoardForm(BaseForm):
    name = StringField(validators=[InputRequired(message=u'请输入版块名称'), Length(2, 10, message=u'版块名称只能为2-10位')])
    board_id = IntegerField(validators=[InputRequired(message=u'没有该板块，不能编辑！')])

# 发布帖子验证
class AddPostForm(BaseForm,Graph_CaptchaForm):
    title = StringField(validators=[InputRequired(message=u'请输入标题'),Length(2,30,message=u'标题长度必须为2-30位')])
    board_id = IntegerField(validators=[InputRequired(message=u'请选择所属板块')])
    content = StringField(validators=[InputRequired(message=u'请输入帖子内容')])

# 帖子加精验证
class ElitePostForm(BaseForm):
    post_id = IntegerField(validators=[InputRequired(message=u'没有该帖子！')])
    elite = IntegerField(validators=[InputRequired(message=u'没有指明需要操作的方式')])

# 帖子评论验证
class AddCommentForm(BaseForm):
    post_id = IntegerField(validators=[InputRequired(message=u'没有该帖子！')])
    content = StringField(validators=[InputRequired(message=u'请输入评论内容！')])
    comment_id = IntegerField()

class PostPraiseForm(BaseForm):
    post_id = IntegerField(validators=[InputRequired(message=u'没有该帖子！')])
    praisenumber = IntegerField(validators=[InputRequired()])