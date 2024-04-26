import hashlib
import bcrypt
import flask
import sqlalchemy.exc

from flask import Flask, render_template, redirect, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user
from data.db_models.cards import Card
from data.db_models import db_session
from data.db_models.users import User
from data.db_models.db_session import global_init, create_session
from data import _utils, cards_api

from data.scripts.reminder import Reminder

app = Flask(__name__)
app.config['SECRET_KEY'] = '.5bB@yqEQF26ZuHcM:/#'

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def index():
    return render_template(f"mainpage/mainpage.html", title="ToDoGenius")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = _utils.SignUpForm()
    if form.validate_on_submit():
        if not form.password.data == form.confirm_password.data:
            return render_template('signup/signup.html',
                                   message='Введённые пароли не совпадают',
                                   form=form)
        session = create_session()
        user = User()

        salt = bcrypt.gensalt()
        hashed_pass = hashlib.md5((form.password.data + salt.decode()).encode()).digest()

        user.nickname = form.nickname.data
        user.birthday = form.birthday.data
        if form.name.data:
            user.name = form.name.data
        user.email = form.email.data
        user.hashed_password = hashed_pass
        user.salt = salt
        try:
            session.add(user)
            session.commit()
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        except sqlalchemy.exc.IntegrityError:
            return render_template('signup/signup.html', form=form, title='Регистрация',
                                   message='Данная электронная почта уже используется')

    return render_template('signup/signup.html', form=form, title='Регистрация')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = _utils.LoginForm()
    if form.validate_on_submit():
        session = create_session()
        password = form.password.data
        user = session.query(User).filter(User.email == form.email.data).first()
        if user:
            salt = user.salt
            if hashlib.md5((password + salt.decode()).encode()).digest() == user.hashed_password:
                login_user(user, remember=form.remember_me.data)
                return redirect('/')
        return render_template('login/login.html', message='Введён неправильный логин или пароль.',
                               title='Авторизация', form=form)
    return render_template('login/login.html', title='Авторизация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = create_session()
    return db_sess.get(User, user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


if __name__ == '__main__':
    global_init('db/database.db')
    app.register_blueprint(cards_api.blueprint)

    reminder = Reminder()
    reminder.start_reminder(8)

    app.run('127.0.0.1', 8080)
