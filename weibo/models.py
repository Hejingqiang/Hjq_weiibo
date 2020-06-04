from User.models import User
from libs.db import db


class Weibo(db.Model):
    __tablename__ = 'weibo'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer)
    content = db.Column(db.Text)
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)

    @property
    def user(self):
        if not hasattr(self, '_user'):
            self._user = User.query.get(self.uid)
        return self._user
