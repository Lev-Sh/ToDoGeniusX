from flask import Flask, render_template
from flask_login import LoginManager
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)


# class LoginForm(FlaskForm):
#    email = EmailField('Почта', validators=[DataRequired()])
#    password = PasswordField('Пароль', validators=[DataRequired()])
#    remember_me = BooleanField('Запомнить меня')
#    submit = SubmitField('Войти')

@login_manager.user_loader
def load_user(user_id):
    return 1


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


@app.route('/')
def index():
    return render_template(f"mainpage/mainpage.html", title="ToDoGenius")


@app.route('/login')
def login():

    return render_template('login/login.html', title='Авторизация')


if __name__ == '__main__':
    app.run('127.0.0.1', 8080)
