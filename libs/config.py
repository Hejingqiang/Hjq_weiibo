
# If you have set Flask.secret_key (or configured it from SECRET_KEY) you can use sessions in Flask applications.
# A session makes it possible to remember information from one request to another.
# The way Flask does this is by using a signed cookie.
# The user can look at the session contents, but can’t modify it unless they know the secret key,
# so make sure to set that to something complex and unguessable.
SECRET_KEY = 'dd9ef07e927825830df31174fc0c999c'


#用于连接数据的数据库
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://chris:Wahjq.666@129.211.74.215:3306/weibo'


#如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它。
SQLALCHEMY_TRACK_MODIFICATIONS = True

PER_PAGE = 30  # 每页微博数量





#自己百度 ORM 和 SQLALCHEMY