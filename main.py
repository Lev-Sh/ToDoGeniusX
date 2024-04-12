import hashlib
import bcrypt

from flask import Flask, render_template
from flask_login import LoginManager, login_user, current_user

from data.__all_models import *
from data.db_session import global_init, create_session
from data import _utils

app = Flask(__name__)
app.config['SECRET_KEY'] = '.5bB@yqEQF26ZuHcM:/#'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = create_session()
    return db_sess.query()


@app.route('/')
def index():
    return render_template(f"mainpage/mainpage.html", title="ToDoGenius")


@app.route('/signup')
def signup():
    form = _utils.SignUpForm()
    if form.validate_on_submit() and form.password.data == form.confirm_password.data:
        session = create_session()
        user = users.User()

        salt = bcrypt.gensalt()
        hashed_pass = hashlib.md5((form.password.data + salt.decode()).encode()).digest()

        user.nickname = form.nickname.data
        user.birthday = form.birthday.data
        if form.name.data:
            user.name = form.name.data
        user.email = form.email.data
        user.hashed_password = hashed_pass
        user.salt = salt

        session.add(user)
        session.commit()
        login_user(user, remember=form.remember_me.data)


@app.route('/login', methods=['GET', 'POST'])
def login():

    return render_template('login/login.html', title='Авторизация')


if __name__ == '__main__':
    global_init('db/users.db')

    app.run('127.0.0.1', 8080)
