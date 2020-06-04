import datetime
from math import ceil

from flask import Blueprint, render_template, request, session, redirect

from libs.config import PER_PAGE
from libs.db import db
from libs.utils import login_required
from weibo.models import Weibo

wb_bp = Blueprint('weibo', import_name='weibo', url_prefix='/weibo')

@wb_bp.route('/post', methods=['get', 'post'])
@login_required
def post():
    if request.method == "POST":
        content = request.form.get('content').strip()
        if not content:
            return render_template('/weibo/post.html',error='内容不能为空')
        uid = session['uid']
        created = datetime.datetime.now()
        weibo = Weibo(uid=uid,content=content,created=created)
        db.session.add(weibo)

        try:
            db.session.commit()
        except Exception as e:
            db.sesion.rollback()
            print(e)
            return render_template('/weibo/post.html',error='服务器内部错误')
        else:
            return redirect(f'/weibo/show?wid={weibo.id}')
    else:
        return render_template('/weibo/post.html')


@wb_bp.route('/show')
def show_weibo():
    wid = int(request.args.get('wid'))
    weibo = Weibo.query.get(wid)
    return render_template('/weibo/show.html',weibo=weibo)


@wb_bp.route('/delete')
@login_required
def delete_weibo():
    wid = int(request.args.get('wid'))
    Weibo.query.filter_by(id=wid).delete()

    try:
        db.session.commit()
    except Exception as e:
        db.sesion.rollback()
        print(e)
        return redirect(f'/weibo/show?wid={wid}&error=服务器内部错误')
    else:
        return redirect('/')

@wb_bp.route('/edit')
@login_required
def edit_weibo():
    if request.method == 'POST':
        wid = request.form.get('wid')
        content = request.form.get('content')

        Weibo.query.filter_by(id=wid).update(content=content)
        try:
            db.session.commit()
        except Exception as e:
            db.sesion.rollback()
            print(e)
            return render_template('/weibo/edit.html',error='服务器内部错误')
        else:
            return redirect(f'/weibo/show?wid={wid}')
    else:
        return render_template('/weibo/post.html')


@wb_bp.route('/list')
def weibo_list():
    page = int(request.args.get('page', 1))
    offset = (page - 1) * PER_PAGE
    weibo_list = Weibo.query.order_by(Weibo.updated.desc()).limit(PER_PAGE).offset(offset)
    total = Weibo.query.count()
    n_page = ceil(total / PER_PAGE)
    return render_template('/weibo/index.html', weibo_list=weibo_list, n_page=n_page, page=page)