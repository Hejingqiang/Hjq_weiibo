import datetime

from flask import Blueprint, render_template, request, session, redirect

from comment.models import Comment
from libs.db import db
from libs.utils import login_required

cmt_bp = Blueprint('comment', import_name='comment', url_prefix='/comment')

@cmt_bp.route('/post', methods=['POST'])
def post():
    '''写评论'''
    uid = session['uid']
    wid = int(request.form.get('wid'))
    cid = int(request.form.get('cid', 0))
    content = request.form.get('content', '').strip()
    created = datetime.datetime.now()

    if not content:
        return render_template(f'/weibo/show?wid={wid}&error=评论内容不为空')

    cmt = Comment(uid=uid, wid=wid, cid=cid, content=content, created=created)
    db.session.add(cmt)

    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        return redirect(f'/weibo/show?wid={wid}&error=评论失败')
    else:
        return redirect(f'/weibo/show?wid={wid}')


@cmt_bp.route('/delete')
@login_required
def delete():
    cid = session['uid']
    cmt = Comment.query.get(cid)

    if cmt.uid == session['uid']:
        db.session.delete(cmt)
        Comment.query.filter_by(cid=cid).update({'cid':0})  # 注意！！将本评论的回复指向微博本身
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
        else:
            return redirect(f'/weibo/show?wid={cmt.wid}')
    else:
        return redirect(f'/weibo/show?wid={cmt.wid}&error=您没有权限删除别人的评论')


