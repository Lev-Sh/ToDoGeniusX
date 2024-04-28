from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, StringField, DateField, FileField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField('Почта *', validators=[DataRequired()])
    password = PasswordField('Пароль *', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class SignUpForm(LoginForm):
    nickname = StringField('Имя пользователя *', validators=[DataRequired()])
    name = StringField('Настоящее имя')
    birthday = DateField('Дата рождения *')
    confirm_password = PasswordField('Подтвердите пароль *', validators=[DataRequired()])
    image = FileField('Добавьте свой аватар', validators=[
        FileRequired(),
        FileAllowed(['png'], 'PNG only!')
    ])
    submit = SubmitField('Зарегистрироваться')
