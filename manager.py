from flask import Flask
from flask_script import Manager

from User.views import user_bp

app = Flask(__name__)

manager = Manager(app=app)

app.register_blueprint(user_bp,url_preix='/user')


if __name__ == '__main__':
    manager.run()
