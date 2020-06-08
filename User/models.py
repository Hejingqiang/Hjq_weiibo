from libs.db import db


class User(db.Model):
    '''用户表'''
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nickname = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(128))
    gender = db.Column(db.String(16))
    city = db.Column(db.String(16))
    avatar = db.Column(db.String(128))
    birthday = db.Column(db.Date, default='2000-01-01')
    bio = db.Column(db.Text())


class Follow(db.Model):
    '''关注表'''
    __tablename__ = 'follow'

    uid = db.Column(db.Integer, primary_key=True)
    fid = db.Column(db.Integer, primary_key=True)

    @classmethod
    def  is_followed(cls, uid, fid):
        '''是否关注对方'''
        query_result = cls.query.filter_by(uid=uid,fid=fid).exists()
        return db.session.query(query_result).scalar()

