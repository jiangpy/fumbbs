#! /usr/bin/env python
# coding:utf-8

from flask import Blueprint
from exts import db
import flask
from models.commonmodels import BoardModel,PostModel,CommentModel,PostPraiseModel,ElitePostModel
from models.frontmodels import FrontUser
from constants import FRONT_SESSION_ID
from decorators.frontdecorators import login_required
from qiniu import Auth
import constants
from utils import myjson
from forms.commonfomrs import AddPostForm,AddCommentForm,PostPraiseForm
import time
bp = Blueprint('front',__name__)


# BBS首页
@bp.route('/')
def index():
    return post_list(1,1,0)

# 帖子列表：
@bp.route('/post_list/<int:c_page>/<int:sort_type>/<int:board_id>/')
def post_list(c_page,sort_type,board_id):
    '''
    帖子分页算法
    start => 切片开始位置
    end => 结束位置
    '''
    start = (c_page-1)*constants.PAGE_NUMBER
    end = start+constants.PAGE_NUMBER
    '''
    sort_type = 1 按发布时间排序（默认是时间排序）
    sort_type = 2 按评论量排序
    sort_type = 3 按是否加精排序
    sort_type = 4 按点赞量排序
    '''
    if sort_type == 1 or not sort_type: # 按发布时间排序（默认是时间排序）
        posts = PostModel.query.order_by(PostModel.create_time.desc())

    elif sort_type ==2: # 按评论量排序
        posts = db.session.query(PostModel).outerjoin(CommentModel).group_by(PostModel.id).order_by(db.func.count(CommentModel.id).desc(),PostModel.create_time.desc())

    elif sort_type == 3: # 按是否加精排序
        posts = db.session.query(PostModel).outerjoin(ElitePostModel).order_by(ElitePostModel.create_time.desc(),PostModel.create_time.desc())

    elif sort_type == 4: # 按点赞量排序
        posts= db.session.query(PostModel).outerjoin(PostPraiseModel).group_by(PostModel.id).order_by(db.func.count(PostPraiseModel.id).desc(),PostModel.create_time.desc())

    posts = posts.filter(PostModel.is_remove==False)
    if int(board_id) != 0:
        posts = posts.filter(PostModel.board_id==board_id)
    boards = BoardModel.query.order_by(BoardModel.create_time.desc()).all()
    post_total = posts.count()
    page_total = post_total / constants.PAGE_NUMBER

    if post_total % constants.PAGE_NUMBER > 0:
        page_total+=1
    page_list =[]
    tmp_page = c_page-1
    # 往前面查找
    while tmp_page >= 1:
        if tmp_page % 5 == 0:
            break
        page_list.append(tmp_page)
        tmp_page -= 1
    # 往后面查找
    tmp_page = c_page
    while tmp_page <= page_total:
        if tmp_page % 5 == 0:
            page_list.append(tmp_page)
            break
        page_list.append(tmp_page)
        tmp_page += 1
    page_list.sort()
    content = {
        'page_total':page_total,
        'c_page':c_page,
        'pages':page_list,
        'boards': boards,
        'sort_type':sort_type,
        'posts': posts.slice(start,end),
        'board_id':board_id,
        'c_url':flask.request.path
    }
    print c_page
    print page_total
    return flask.render_template('front/front_index.html', **content)

# 帖子详情
@bp.route('/postdetail/<int:post_id>/')
def post_detail(post_id):
    postmodel = PostModel.query.filter(PostModel.is_remove==False,PostModel.id==post_id).first()
    if not postmodel:
        flask.abort(404)
    postmodel.read_count += 1
    db.session.commit()
    post_praise_author_ids =[ praise.author.uid for praise in postmodel.praises]
    comments = CommentModel.query.filter_by(post_id=post_id).order_by(CommentModel.create_time.desc())
    content = {
        'post':postmodel,
        'comments':comments,
        'post_praise_author_ids':post_praise_author_ids,
        'c_url':flask.request.path
    }
    return flask.render_template('front/front_postdetail.html',**content)


# 点赞功能
@bp.route('/post_praise/',methods=['POST'])
@login_required
def post_praise():
    form = PostPraiseForm(flask.request.form)
    if form.validate():
        post_id = form.post_id.data
        praisenumber = form.praisenumber.data
        postModel = PostModel.query.get(post_id)
        pariseModel = PostPraiseModel.query.filter_by(post_id=post_id, author_id=flask.g.front_user.uid).first()
        c_url = flask.url_for('front.post_detail',post_id=post_id)
        if praisenumber == 0:
            if pariseModel:
                return myjson.json_params_error(u'您已经给这篇帖子点过赞了！不能重复点赞！')
            post_praise = PostPraiseModel()
            post_praise.post = postModel
            post_praise.author = flask.g.front_user
            db.session.add(post_praise)
            db.session.commit()
            return myjson.json_result()
        else:
            if pariseModel:
                db.session.delete(pariseModel)
                db.session.commit()
                return myjson.json_result()
            else:
                return myjson.json_params_error(u'您尚未对该帖子点赞！')
    else:
        return myjson.json_params_error(form.get_error())



# 发布新帖子！
@bp.route('/addpost/',methods = ['GET','POST'])
@login_required
def addpost():
    if flask.request.method == 'GET':
        boards = BoardModel.query.order_by(BoardModel.create_time.desc()).all()
        content = {
            'boards': boards
        }
        return flask.render_template('front/front_addpost.html',**content)
    else:
        form = AddPostForm(flask.request.form)
        if form.validate():
            title = form.title.data
            board_id = form.board_id.data
            content = form.content.data
            postmodel = PostModel(title=title,content=content)
            boardmodel = BoardModel.query.filter_by(id=board_id).first()
            if not boardmodel:
                return myjson.json_params_error(message=u'板块不存在，请重新选择所属板块！')
            postmodel.board = boardmodel
            postmodel.author = flask.g.front_user
            db.session.add(postmodel)
            db.session.commit()
            post = PostModel.query.first()
            return myjson.json_result()

        else:
            return myjson.json_params_error(message=form.get_error())

# 七牛上传图片视频的token 获取
@bp.route('/get_qiniu_token/')
def get_qiniu_token():
    q = Auth(constants.ACCESSKEY,constants.SECRETKEY)
    buckt_name = 'fumbbs'
    token = q.upload_token(bucket=buckt_name)
    return flask.jsonify({'uptoken':token})


# 发表帖子评论
@bp.route('/addcomment/<int:post_id>/',methods=['GET',"POST"])
@login_required
def add_comment(post_id):
    if flask.request.method == 'GET':
        comment_id = flask.request.args.get('commentid')
        content = {
            'post':PostModel.query.get(post_id),
        }
        if comment_id:
            commentModel = CommentModel.query.get(comment_id)
            content['comment'] = commentModel
        return flask.render_template('front/front_post_comment.html',**content)
    else:
        form = AddCommentForm(flask.request.form)
        if form.validate():
            post_id = form.post_id.data
            content = form.content.data
            comment_id = form.comment_id.data
            print  comment_id
            comment = CommentModel(content=content)
            post = PostModel.query.filter_by(id=post_id).first()
            if not post:
                return myjson.json_result(message=u'该帖子不存在!无法评论！')
            comment.post = post
            comment.author = flask.g.front_user
            if comment_id:
                origin_comment = CommentModel.query.get(comment_id)
                comment.origin_comment = origin_comment
            db.session.add(comment)
            db.session.commit()
            return myjson.json_result()
        else:
            return myjson.json_params_error(message=form.get_error())




@bp.errorhandler(401)
def post_auth_forbidden(error):
    if flask.request.is_xhr:
        return myjson.json_unauth_error(u'权限不允许')
    else:
        return flask.render_template('common/401.html'),401

@bp.errorhandler(404)
def post_found(error):
    if flask.request.is_xhr:
        return myjson.json_params_error(u'页面没找到！')
    else:
        return flask.render_template('common/404.html'),404