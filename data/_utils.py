from string import ascii_lowercase

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, StringField, DateField, FileField
from wtforms.validators import DataRequired

RUSSIAN_ALPHABET = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
SPECIAL_SYMBOLS = '!@#$%^&*()_-+=,./;:|?><`~{}[]'


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
        FileAllowed(['png'], 'PNG only!')
    ])
    submit = SubmitField('Зарегистрироваться')


def check_password_complexity(password: str) -> bool:
    special = 0
    letters = 0
    numbers = 0
    uppercase = 0

    for symbol in password:
        if symbol.lower() in ascii_lowercase or symbol.lower() in RUSSIAN_ALPHABET:
            letters += 1
            if symbol.isupper():
                uppercase += 1
        elif symbol.isdigit():
            numbers += 1
        elif symbol in SPECIAL_SYMBOLS:
            special += 1

    if len(password) >= 8 and special > 0 and letters > 0 and numbers > 0 and uppercase > 0:
        return True
    return False
