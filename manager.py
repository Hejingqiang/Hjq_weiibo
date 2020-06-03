from flask import Flask, render_template
from flask_migrate import MigrateCommand, Migrate
from flask_script import Manager

from User.views import user_bp
from libs import config
from libs.db import db

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

migrate = Migrate(app, db)

manager = Manager(app=app)
manager.add_command('db', MigrateCommand)

app.register_blueprint(user_bp)


@app.route('/')
def home():
    return render_template('base.html')


if __name__ == '__main__':
    manager.run()
