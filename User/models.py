from libs.db import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nickname = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(128))
    gender = db.Column(db.String(16))
    city = db.Column(db.String(16))
    avatar = db.Column(db.String(128))
    birthday = db.Column(db.Date, default='2000-01-01')
    bio = db.Column(db.Text())
