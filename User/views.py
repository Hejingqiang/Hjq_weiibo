from flask import Blueprint, render_template, request, redirect, session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from User.models import User
from libs import utils
from libs.db import db


user_bp = Blueprint('user',import_name='user',url_prefix='/user')


@user_bp.route('/register',methods=['GET','POST'])
def register():
    '''注册'''
    if request.method == 'POST':
        nickname = request.form.get('nickname','').strip()
        password = request.form.get('password','').strip()
        gender = request.form.get('gender','').strip()
        city = request.form.get('city','北京')
        avatar = request.files.get('avatar','').strip()
        birthday = request.form.get('birthday','2000-10-10').strip()
        bio = request.form.get('bio', '').strip()

        if not(nickname and password):
            return render_template('/user/register.html',error='昵称和密码不能为空')

        #密码处理
        safe_password = utils.make_password(password)
        avatar_url = utils.ave_avatar(nickname, avatar)
        user = User(nickname=nickname,
                    password=safe_password,
                    gender=gender,
                    city=city,
                    avatar=avatar,
                    birthday=birthday,
                    bio=bio
                    )

        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:  # 例： IntegrityError: (1062, "Duplicate entry 'xx' for key 'xxxxx'")
            db.session.rollback()
            return render_template('/user/register.html', error='昵称和密码不能为空')
        return redirect('/user/login')
    else:
        return render_template('/user/register.html')





@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    '''登录'''
    if request.method == 'POST':
        nickname = request.form.get('nickname', '').strip()
        password = request.form.get('password', '').strip()

        if not (nickname and password):
            return render_template('login.html', error='昵称或密码不能为空')

        try:
            user = User.query.filter_by(nickname=nickname).one()  # 不加.one（）的结果是一个列表，而不是实例对象，所以即使只取到一个结果还是要遍历列表，故！要加.one（）来取列表中实例对象
        except (NoResultFound, MultipleResultsFound):  # 错误
            return render_template('/user/login.html')

        if utils.check_password(password, user.password):
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
    '''显示个人信息'''
    user = User.query.get(session['uid'])
    return render_template('/user/info.html', user=user)





