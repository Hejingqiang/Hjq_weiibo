from flask import Blueprint, render_template, request, redirect, session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from User.models import User, Follow
from libs import utils
from libs.db import db
from libs.utils import login_required

user_bp = Blueprint('user',import_name='user',url_prefix='/user')


@user_bp.route('/register',methods=['GET','POST'])
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
            return render_template('register.html', error='昵称或密码不为空')

        safe_password = utils.make_password(password)  # 安全处理密码
        avatar_url = utils.save_avatar(nickname, avatar)  # 保存头像，并返回头像网址

        user = User(nickname=nickname, password=safe_password, gender=gender,
                    city=city, avatar=avatar_url, birthday=birthday, bio=bio)

        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:  # 例： IntegrityError: (1062, "Duplicate entry 'xx' for key 'xxxxx'")
            db.session.rollback()
            return render_template('/user/register.html', error='昵称和密码能为空')
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

@user_bp.route('/follow')
def follow():
    '''关注/取消关注'''
    fid = int(request.args.get('fid'))
    uid = session['uid']

    follow_relation = Follow(uid=uid,fid=fid)
    db.session.add(follow_relation)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()  # 发生冲突时，说明已经关注过此人，需要取消关注

        Follow.query.filter_by(uid=uid, fid=fid).delete()  # 取消关注，删除两人的关系
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()

    return redirect(f'/user/info?uid={fid}')


@user_bp.route('/fans')
@login_required
def fans():
    '''查看自己的粉丝列表'''
    uid = session['uid']

    # select uid from follow where fid=7;
    fans_uid_list = Follow.query.filter_by(fid=uid).values('uid')
    fans_uid_list = [f[0] for f in fans_uid_list]

    fans = User.query.filter(User.id.in_(fans_uid_list))
    return render_template('/user/fans.html', fans=fans)


@user_bp.route('/followee')
@utils.login_required
def followee():
    '''查看自己关注的人'''
    uid = session['uid']

    follow_uid_list = Follow.query.filter_by(uid=uid).values('fid')
    follow_uid_list = [f[0] for f in follow_uid_list]

    followee = User.query.filter(User.id.in_(follow_uid_list))
    return render_template('/user/followee.html', followee=followee)






