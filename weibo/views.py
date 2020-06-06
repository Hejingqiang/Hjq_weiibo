import datetime
from math import ceil

from flask import Blueprint, render_template, request, session, redirect
from sqlalchemy.exc import IntegrityError

from comment.models import Comment
from libs.config import PER_PAGE
from libs.db import db
from libs.utils import login_required
from weibo.models import Weibo, Like

wb_bp = Blueprint('weibo', import_name='weibo', url_prefix='/weibo')


@wb_bp.route('/post', methods=['GET','POST'])
@login_required
def post_weibo():
    '''发布微博'''
    if request.method == 'POST':
        uid = session['uid']
        content = request.form.get('content')
        if not content:
            return render_template('/weibo/post.html', error='内容不能为空')
        created = datetime.datetime.now()
        updated = datetime.datetime.now()

        weibo = Weibo(uid=uid, content=content, created=created, updated=updated)
        db.session.add(weibo)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
            return render_template('/weibo/post.html', error='服务器内部错误')
        else:
            return redirect(f'/weibo/show?wid={weibo.id}')  # 微博显示页面
    else:
        return render_template('/weibo/post.html')


@wb_bp.route('/edit', methods=['GET','POST'])
@login_required
def edit_weibo():
    '''编辑微博'''
    if request.method == 'POST':
        wid = request.form.get('wid')
        content = request.form.get('content')
        updated = datetime.datetime.now()

        if not content:
            return render_template('/weibo/edit.html', error='内容不能为空')

        weibo = Weibo.query.filter_by(id=wid).update({Weibo.content:content,Weibo.updated:updated})

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
            return render_template('/weibo/edit.html', error='服务器内部错误')
        else:
            return redirect(f'/weibo/show?wid={wid}')  # 微博显示页面
    else:
        wid = int(request.args.get('wid'))
        weibo = Weibo.query.get(wid)
        return render_template('/weibo/edit.html',weibo=weibo)

@wb_bp.route('/show')
def show_weibo():
    '''显示微博'''
    wid = int(request.args.get('wid'))
    weibo = Weibo.query.get(wid)
    return render_template('/weibo/show.html',weibo=weibo)


@wb_bp.route('/delete')
@login_required
def delete_weibo():
    '''删除微博'''
    wid = int(request.args.get('wid'))
    weibo = Weibo.query.get(wid)

    #是否有权限
    if weibo.uid != session['uid']:
        return redirect(f'/weibo/show?wid={wid}&error=无权删除他人微博')
    # 关联删除当前微博的评论和赞
    Comment.query.filter_by(wid=wid).delete()
    Like.query.filter_by(wid=wid).delete()
    db.session.delete(weibo)
    try:
        db.session.commit()
    except Exception as e:
        db.sesion.rollback()
        print(e)
        return redirect(f'/weibo/show?wid={wid}&error=服务器内部错误')
    else:
        return redirect('/')


@wb_bp.route('/list')
def weibo_list():
    '''微博列表'''
    page = int(request.args.get('page', 1))
    offset = (page - 1) * PER_PAGE
    weibo_list = Weibo.query.order_by(Weibo.updated.desc()).limit(PER_PAGE).offset(offset)
    total = Weibo.query.count()
    n_page = ceil(total / PER_PAGE)
    return render_template('/weibo/index.html', weibo_list=weibo_list, n_page=n_page, page=page)

#分页器：设置每页数目 偏移量 总页数 总条数 当前页


@wb_bp.route('/like')
@login_required
def like():
    uid = session['uid']
    wid = int(request.args.get('wid'))
    from_url = request.args.get('from')

    like_wb = Like(uid=uid,wid=wid)
    Weibo.query.filter_by(id=wid).update({'n_like':Weibo.n_like + 1})

    db.session.add(like_wb)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

        Like.query.filter_by(uid=uid,wid=wid).delete()
        Weibo.query.filter_by(id=wid).update({'n_like':Weibo.n_like - 1})
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
    return redirect(from_url)
