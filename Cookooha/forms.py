from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, PasswordField, validators



def password_check(form, field):
    pass


class LoginForm(FlaskForm):
    pass


class RegistrationForm(FlaskForm):
    username = StringField('Имя', [validators.DataRequired()])
    email = StringField('e-mail')
    password = PasswordField('Пароль', [validators.DataRequired()])


class ChangePasswordForm(FlaskForm):
    pass
