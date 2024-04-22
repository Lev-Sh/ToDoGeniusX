from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, StringField, DateField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField('Почта *', validators=[DataRequired()])
    password = PasswordField('Пароль *', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class SignUpForm(LoginForm):
    nickname = StringField('Имя пользователя *')
    name = StringField('Настоящее имя')
    birthday = DateField('Дата рождения')
    confirm_password = PasswordField('Подтвердите пароль *')
    submit = SubmitField('Зарегистрироваться')
