from User.models import User
from libs.db import db


class Weibo(db.Model):
    '''微博表'''
    __tablename__ = 'weibo'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer)
    content = db.Column(db.Text)
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)

    # 点赞数
    n_like = db.Column(db.Integer, default=0)

    @property  # 外键==》property!!!!!!!
    def user(self):
        '''当前微博作者'''
        if not hasattr(self, '_user'):
            self._user = User.query.get(self.uid)
        return self._user


class Like(db.Model):
    ''''点赞表'''
    __tablename__ = 'like'

    uid = db.Column(db.Integer, primary_key=True)
    wid = db.Column(db.Integer, primary_key=True)

    @classmethod
    def is_liked(cls,uid,wid):
        '''检查是否已存在赞'''
        base_query = Like.query.filter_by(uid=uid, wid=wid).exists()
        return db.session.query(base_query).scalar()

