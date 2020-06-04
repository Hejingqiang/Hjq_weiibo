from flask import Flask, redirect
from flask_migrate import MigrateCommand, Migrate
from flask_script import Manager

from User.views import user_bp
from libs import config
from libs.db import db
from libs.utils import fake_word, fake_sentence
from weibo.views import wb_bp

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

migrate = Migrate(app, db)

manager = Manager(app=app)
manager.add_command('db', MigrateCommand)

app.register_blueprint(user_bp)
app.register_blueprint(wb_bp)


@app.route('/')
def home():
    return redirect('/weibo/list')


@manager.command
def fake():
    import random
    from User.models import User
    from weibo.models import Weibo


    users = []

    for i in range(20):
        user = User(
            nickname=fake_word().title(),
            gender=random.choice(['male', 'female', 'unknow']),
            city=random.choice(['北京', '上海', '深圳']),
            avatar='/static/upload/default',
            birthday='1996-06-13',
            bio=fake_sentence(),
        )
        users.append(user)
    db.session.add_all()
    db.session.commit()

    weibo_list = []
    for i in range(1000):
        y = random.randint(2000, 2020)
        m = random.randint(1, 12)
        d = random.randint(1, 28)
        date = '%d-%02d-%02d' % (y, m, d)

        weibo = Weibo(
            uid=random.choice(users).id,
            content=fake_sentence(),
            created=date,
            updated=date,
        )
        weibo_list.append(weibo)

    db.session.add_all(weibo_list)
    db.session.commit()

if __name__ == '__main__':
    manager.run()
