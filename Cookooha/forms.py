from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, PasswordField, validators



def password_check(form, field):
    pass


class LoginForm(FlaskForm):
    pass


class RegistrationForm(FlaskForm):
    username = StringField('Имя', [validators.DataRequired()])
    password = PasswordField('Пароль', [validators.DataRequired(), validators.EqualTo('confirm', message='Введите пароль!')])
    confirm = PasswordField('Повторите пароль')
    submit = SubmitField('Подтвердить')

class ChangePasswordForm(FlaskForm):
    pass