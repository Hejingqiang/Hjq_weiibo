from flask import Blueprint, render_template, request, redirect, session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from User.models import User
from libs import utils
from libs.db import db

user_bp = Blueprint('user',import_name='user',url_prefix='/user')


@user_bp.route('/register',methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nickname = request.form.get('nickname','').strip()
        passwd = request.form.get('passwd','').strip()
        gender = request.form.get('gender','unknow').strip()
        city = request.form.get('city','上海').strip()
        avatar = request.files.get('avatar')
        birthday = request.form.get('birthday','2000-01-01')
        bio = request.form.get('bio','').strip()

        if not (nickname and passwd):
            return render_template('/user/register.html',error='昵称密码不可为空')

        safe_passwd = utils.make_passwd(passwd)
        avatar_url = utils.save_avatar(nickname,avatar)

        user = User(nickname=nickname,passwd=safe_passwd,gender=gender,city=city,avatar=avatar_url,birthday=birthday,bio=bio)

        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return render_template('/user/register.html',error='昵称密码不可为空')
        return redirect('/user/login')
    else:
        return render_template('/user/register.html')

@user_bp.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        nickname = request.form.get('nickname','').strip()
        passwd = request.form.get('passwd','').strip()

        if not (nickname and passwd):
            return render_template('/user/login.html', error='昵称或密码不能为空')

        try:
            user = User.query.filter_by(nickname).one()
        except (NoResultFound, MultipleResultsFound):
            return render_template('/user/login.html', error='昵称或密码输入错误')

        if utils.check_passwd(passwd, user.password):
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




