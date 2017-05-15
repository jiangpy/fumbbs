#! /usr/bin/env python
# coding:utf-8
from exts import db
import datetime
from frontmodels import FrontUser
from cmsmodels import CMSUser

# 板块模型
class BoardModel(db.Model):
    __tablename__ = 'boards'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(50),nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.datetime.now)
    edit_time = db.Column(db.DateTime)
    author_id = db.Column(db.String(100),db.ForeignKey('cmsuser.uid'))
    author = db.relationship('CMSUser',backref='boards')


# 帖子模型
class PostModel(db.Model):
    __tablename__='post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.datetime.now)
    read_count = db.Column(db.Integer,default=0)
    is_remove = db.Column(db.Boolean,default=False)
    updat_time = db.Column(db.DateTime,default=datetime.datetime.now,onupdate=datetime.datetime.now)
    board_id = db.Column(db.Integer,db.ForeignKey('boards.id'))
    author_id = db.Column(db.String(100),db.ForeignKey('front_user.uid'))
    is_elite_id =db.Column(db.Integer,db.ForeignKey('elitepost.id'))


    board = db.relationship('BoardModel',backref=db.backref('posts',lazy='dynamic'))
    author = db.relationship('FrontUser',backref='posts')
    is_elite=db.relationship('ElitePostModel',backref='post',uselist=False)

# 是否加精```
class ElitePostModel(db.Model):
    __tablename__ = 'elitepost'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime,default=datetime.datetime.now)
    create_user_id = db.Column(db.String(100),db.ForeignKey('cmsuser.uid'))

    create_user = db.relationship('CMSUser',backref='is_elite')

# 帖子评论
class CommentModel(db.Model):
    __tablename__='comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    content = db.Column(db.Text, nullable=False)
    is_removed = db.Column(db.Boolean,default=False)
    author_id  = db.Column(db.String(100),db.ForeignKey('front_user.uid'))
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'))
    origin_comment_id = db.Column(db.Integer,db.ForeignKey('comment.id'))

    author  = db.relationship('FrontUser',backref='comments')
    post = db.relationship('PostModel',backref='comments')
    origin_comment = db.relationship("CommentModel",remote_side=[id],backref='replys')


# 帖子点赞
class PostPraiseModel(db.Model):
    __tablename__ = 'postpraise'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    author_id = db.Column(db.String(100),db.ForeignKey('front_user.uid'))
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'))

    author = db.relationship('FrontUser',backref = 'praises')
    post = db.relationship('PostModel',backref = 'praises')
