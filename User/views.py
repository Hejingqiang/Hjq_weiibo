from flask import Blueprint, render_template, request, redirect, session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from User.models import User
from libs import utils
from libs.db import db

user_bp = Blueprint('user',import_name='user',url_prefix='/user')


@user_bp.route('/register', methods=('GET', 'POST'))
def register():
    '''注册'''
    if request.method == 'POST':
        nickname = request.form.get('nickname', '').strip()
        password = request.form.get('password', '').strip()
        gender = request.form.get('gender', 'unknow').strip()
        city = request.form.get('city', '上海').strip()
        avatar = request.files.get('avatar')
        birthday = request.form.get('birthday', '2000-01-01').strip()
        bio = request.form.get('bio', '').strip()

        if not (nickname and password):
            return render_template('/user/register.html', error='昵称或密码不能为空')

        safe_password = utils.make_password(password)  # 安全处理密码
        avatar_url = utils.save_avatar(nickname, avatar)  # 保存头像，并返回头像网址

        user = User(nickname=nickname, password=safe_password, gender=gender,
                    city=city,avatar=avatar_url,birthday=birthday,bio=bio)

        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()  # 操作失败，进行事务回滚
            return render_template('/user/register.html', error='昵称或密码不能为空')
        return redirect('/user/login')
    else:
        return render_template('/user/register.html')



@user_bp.route('/login', methods=('POST', 'GET'))
def login():
    '''登录'''
    if request.method == 'POST':
        nickname = request.form.get('nickname', '').strip()
        password = request.form.get('password', '').strip()

        if not (nickname and password):
            return render_template('/user/login.html', error='昵称或密码不能为空')

        # 先根据昵称取到当前用户
        try:
            user = User.query.filter_by(nickname=nickname).one()
        except (NoResultFound, MultipleResultsFound):
            return render_template('/user/login.html', error='昵称或密码输入错误')

        # 检查密码
        if utils.check_password(password, user.password):
            # 登录
            session['uid'] = user.id
            session['nickname'] = user.nickname
            return redirect('/user/info')
        else:
            return render_template('/user/login.html', error='昵称或密码输入错误')
    else:
        return render_template('/user/login.html')

@user_bp.route('/info')
@utils.login_required
def info():
    user = User.query.get(session['uid'])
    return render_template('/user/info.html', user=user)





