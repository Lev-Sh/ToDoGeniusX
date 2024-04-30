import hashlib
import io
import os
from threading import Thread

import bcrypt
import flask
import sqlalchemy.exc

from PIL import Image
from flask import Flask, render_template, redirect, jsonify, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data.db_models.notifications import Notification
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
    if current_user.is_authenticated:
        for notification in current_user.notification:
            if notification.seen == 0:
                return render_template(f"mainpage/mainpage.html", title="ToDoGenius", point=True)
        return render_template(f"mainpage/mainpage.html", title="ToDoGenius", point=False)

    return render_template(f"mainpage/mainpage.html", title="ToDoGenius", point=False)


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
        if form.birthday.data:
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
            if form.image.data:
                with open(f'static/profile_imgs/{current_user.id}.png', 'wb') as img_file:
                    img_file.write(form.image.data.read())
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


@app.route('/profile')
@login_required
def profile():
    user = current_user
    user_id = user.id
    user_photo = None

    for image in os.listdir('static/profile_imgs'):
        if image[:image.rfind('.')] == str(user_id):
            user_photo = image
            break

    params = {
        'title': f"{user.nickname}'s profile",
        'photo': user_photo,
        'nickname': f'{user.nickname}#{user.id}',
        'name': user.name,
        'birthday': user.birthday,
        'email': user.email,
    }

    return render_template('profile/profile.html', **params)


@app.route('/notifications')
@login_required
def notifications():
    session = create_session()
    params = {
        'notifications': current_user.notification
    }

    for notification in current_user.notification:
        notification = session.get(Notification, notification.id)
        notification.seen = 1

    session.commit()

    return render_template('profile/notifications.html', **params)


@app.route('/change_profile/<item>', methods=['GET', 'POST'])
@login_required
def change_profile(item):
    if request.method == 'GET':
        titles = {
            'nickname': 'Изменение имени пользователя',
            'name': 'Изменение имени',
            'email': 'Изменение адреса электронной почты',
            'birthday': 'Изменение даты рождения'
        }

        if item == 'image':
            return redirect('/photo_loader/profile')
        else:
            return render_template('login/change_info.html', item=item, title=titles[item])
    elif request.method == 'POST':
        session = create_session()
        db_user = session.query(User).filter(User.email == current_user.email).first()
        if 'name' in request.form:
            db_user.name = request.form['name']
        elif 'nickname' in request.form:
            db_user.nickname = request.form['nickname']
        elif 'email' in request.form:
            db_user.email = request.form['email']
        elif 'birthday' in request.form:
            db_user.birthday = request.form['birthday']

        session.commit()

        return redirect('/profile')


@login_manager.user_loader
def load_user(user_id):
    db_sess = create_session()
    return db_sess.get(User, user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/photo_loader/<page>', methods=['GET', 'POST'])
@login_required
def photo_loader(page):
    if request.method == 'GET':
        return render_template('login/photo_loader.html', title='Загрузка фото')
    elif request.method == 'POST':
        f = request.files['image']
        image = Image.open(io.BytesIO(f.read()))
        image = image.resize((200, 200))
        image.save(f'static/profile_imgs/{current_user.id}.png', 'png')
        return redirect(f'/{page}')


if __name__ == '__main__':
    global_init('db/database.db')
    app.register_blueprint(cards_api.blueprint)

    reminder = Reminder()
    reminder.start_reminder(2)

    app.run('127.0.0.1', 8080)
