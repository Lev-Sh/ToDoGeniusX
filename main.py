import hashlib
import bcrypt

from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, current_user

from data.users import User
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


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = _utils.SignUpForm()
    if form.validate_on_submit():
        if not form.password.data == form.confirm_password.data:
            pass
            # return render_template('login/login.html',
            #                        message='Введённые пароли не совпадают',
            #                        form=form)
        session = create_session()
        user = User()

        salt = bcrypt.gensalt()
        hashed_pass = hashlib.md5((form.password.data + salt.decode()).encode()).digest()

        # user.nickname = form.nickname.data
        # user.birthday = form.birthday.data
        # if form.name.data:
        #     user.name = form.name.data
        user.email = form.email.data
        user.hashed_password = hashed_pass
        user.salt = salt

        session.add(user)
        session.commit()

        login_user(user, remember=form.remember_me.data)

        return redirect('/')

    return render_template('signup/signuph.html', form=form, title='Регистрация')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = _utils.LoginForm()
    if form.validate_on_submit():
        session = create_session()
        password = form.password.data
        user = session.query(User).filter(User.email == form.email.data).first()
        salt = user.salt
        if hashlib.md5((password + salt.decode()).encode()).digest() == user.hashed_password:
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login/login.html', message='Введён неправильный пароль',
                               title='Авторизация', form=form)
    return render_template('login/login.html', title='Авторизация', form=form)


if __name__ == '__main__':
    global_init('db/users.db')

    app.run('127.0.0.1', 8080)
