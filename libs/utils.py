import os
import random
import string
from functools import wraps
from hashlib import sha256

from flask import session, redirect


def make_password(password):
    '''密码加密处理'''
    if not isinstance(password, bytes):
        password = str(password).encode('utf-8')

    safe_password = os.urandom(16).hex() + sha256(password).hexdigest()
    return safe_password


def check_password(password, safe_password):
    '''密码校验'''
    if not isinstance(password,bytes):
        password = str(password).encode('utf-8')

    #加盐
    hash_password = sha256(password).hexdigest()
    return hash_password == safe_password[32:]



def save_avatar(nickname, avatar):
    '''头像保存到硬盘'''
    base_dir = os.path.dirname(os.path.abspath(__name__))
    filepath = os.path.join(base_dir, 'static', 'upload', nickname)
    avatar.save(filepath)
    avatar_url = f'/static/upload/{nickname}'
    return avatar_url


def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if isinstance(session.get('uid'), int):
            return  view_func(*args, **kwargs)
        else:
            return redirect('/user/login')
    return wrapper


def fake_word():
    n_chars = random.randint(4,8)
    chars = random.choices(string.ascii_lowercase, k=n_chars)
    return ''.join(chars)


def fake_sentence():
    n_words = random.randint(10, 20)
    sentence = ' '.join(fake_word() for i in range(n_words))
    sentence = sentence.capitalize() + '.'
    return sentence