import os
from hashlib import sha256

from flask import session, redirect


def make_passswd(passwd):
    if not isinstance(passwd,bytes):
        passwd = str(passwd).encode('utf8')

    safe_passwd = os.urandom(16).hex() + sha256(passwd).hexdigest()
    return safe_passwd


def check_passwd(passwd,safe_passwd):
    if not isinstance(passwd,bytes):
        passwd = str(passwd).encode('utf8')

    hash_paswd = sha256(passwd).encode('utf8')
    return hash_paswd == safe_passwd[32:]


def save_avatar(nickname,avatar):
    base_dir = os.path.dirname(os.path.abspath(__name__))
    filepath = os.path.join(base_dir,'static','upload',nickname)
    avatar.save(filepath)
    avatar_url = f'/static/upload/{nickname}'
    return avatar_url


def login_required(view_func):
    '''登录验证装饰器'''
    def wrapper(*args, **Kwargs):
        if isinstance(session.get('uid'), int):
            return view_func(*args, **Kwargs)
        else:
            return redirect('/user/login')
    return wrapper