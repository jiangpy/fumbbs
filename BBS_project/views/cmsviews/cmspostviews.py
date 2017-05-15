#! /usr/bin/env python
# coding:utf-8

from cms_exts import bp
from models.commonmodels import BoardModel,PostModel,ElitePostModel
import flask
from exts import db
from utils import myjson
from decorators.cmsdecorators import login_required
from forms.commonfomrs import AddBoardForm,EditBoardForm,ElitePostForm
import datetime
import constants



@bp.route('/')
@login_required
def index():
    return flask.render_template('cms/cms_index.html')

# 板块管理
@bp.route('/boards_manage/', methods=['GET','POST'])
@login_required
def boards_manage():
    if flask.request.method == 'GET':
        boards = BoardModel.query.order_by(BoardModel.create_time.desc()).all()
        return flask.render_template('cms/cms_boards_manage.html', boards=boards)

# 添加板块
@bp.route('/add_board/',methods=['POST'])
@login_required
def add_board():
    form = AddBoardForm(flask.request.form)
    if form.validate():
        name = flask.request.form.get('name')
        if BoardModel.query.filter_by(name=name).first():
            return myjson.json_params_error(message=u'该板块已经存在，不能重复添加！')
        boardsModel = BoardModel(name=name)
        boardsModel.author = flask.g.cms_user
        db.session.add(boardsModel)
        db.session.commit()
        return myjson.json_result()
    else:
        return myjson.json_params_error(message=form.get_error())

# 编辑板块
@bp.route('/edit_board/',methods=['POST'])
@login_required
def edif_board():
    form = EditBoardForm(flask.request.form)
    if form.validate():
        name = form.name.data
        board_id = form.board_id.data
        boardModel = BoardModel.query.get(board_id)
        if not boardModel:
            return myjson.json_params_error(message=u'板块不存在，无法编辑！')
        boardModel.name = name
        boardModel.author = flask.g.cms_user
        boardModel.edit_time = datetime.datetime.now()
        db.session.commit()
        return myjson.json_result()
    else:
        return myjson.json_params_error(message=form.get_error())

# 删除板块
@bp.route('/delete_board/',methods=['POST'])
@login_required
def delete_board():
    board_id = flask.request.form.get('board_id')
    boardModel= BoardModel.query.get(board_id)
    if not boardModel:
        return myjson.json_params_error(message=u'板块不存在，无法删除！')
    db.session.delete(boardModel)
    db.session.commit()
    return myjson.json_result()

# 帖子列表
@bp.route('/posts/')
def posts():
    return post_list(2)


# 帖子列表分页/排序
@bp.route('/post_list/')
@login_required
def post_list():
    # 每页显示帖子切片位置

    '''
            sort_type = 1 按发布时间排序
            sort_type = 2 按评论量排序
            sort_type = 3 按加精排序
    '''
    sort_type = flask.request.args.get('sort',type=int)
    board_id = flask.request.args.get('board',0,type=int)
    c_page = flask.request.args.get('page',1,type=int)
    start = (c_page - 1) * constants.PAGE_NUMBER
    end = start + constants.PAGE_NUMBER
    if not sort_type or sort_type == 1:
        posts = PostModel.query.order_by(PostModel.create_time.desc())
    elif sort_type == 2:
        posts = PostModel.query.order_by(PostModel.create_time.desc())
    elif sort_type == 3:
        posts = db.session.query(PostModel).outerjoin(ElitePostModel).order_by(ElitePostModel.create_time.desc(),PostModel.create_time.desc())
    if board_id != 0:
        posts = posts.filter(PostModel.board_id==board_id)

    '''
        分页算法
    '''
    # 当前帖子总数
    post_number = posts.count()
    # 总页数
    total_page = post_number / constants.PAGE_NUMBER
    if post_number % constants.PAGE_NUMBER != 0:
        total_page += 1
    # 根据当前页面计算当前显示多少翻页标签
    page_list = []
    # 根据当前页面往前面找
    tmp_page = c_page - 1
    while tmp_page >= 1:
        if tmp_page % 5 == 0:
            break
        page_list.append(tmp_page)
        tmp_page -= 1
    # 往后面找
    tmp_page = c_page
    while tmp_page <= total_page:
        if tmp_page % 5 == 0:
            page_list.append(tmp_page)
            break
        page_list.append(tmp_page)
        tmp_page += 1
    page_list.sort()
    boards = BoardModel.query.all()
    posts = posts.slice(start, end)
    content = {
        'page_list':page_list,
        'c_page':c_page,
        'total_page':total_page,
        'posts':posts,
        'boards':boards,
        'c_board_id':board_id,
        'sort':sort_type,
    }
    return flask.render_template('cms/cms_post_list.html',**content)


# 加精/取消加精
@bp.route('/elite/',methods=['POST'])
@login_required
def elite():
    form = ElitePostForm(flask.request.form)
    if form.validate():
        '''
            elite == 0  代表当前帖子没有加精
            elite == 1 代表当前帖子已经加精
        '''
        post_id  = form.post_id.data
        elite = form.elite.data
        postModel = PostModel.query.filter_by(id=post_id).first()
        if not postModel:
            return myjson.json_params_error(u'没有该篇帖子')
        if elite == 0:
            print postModel.is_elite
            eliteModel = ElitePostModel()
            eliteModel.create_user = flask.g.cms_user
            postModel.is_elite = eliteModel
            db.session.commit()
            return myjson.json_result()
        if elite == 1:
            db.session.delete(postModel.is_elite)
            db.session.commit()
            return myjson.json_result()

    else:
        return myjson.json_params_error(form.get_error())


#移除帖子
@bp.route('/delete_post/',methods=['POST'])
def delete_post():
    post_id = flask.request.form.get('post_id')
    postModel = PostModel.query.filter_by(id=post_id).first()
    print post_id
    if not post_id or not postModel:
        return myjson.json_params_error(message=u'该帖子不存在！')
    postModel.is_remove = True
    db.session.commit()
    return myjson.json_result()