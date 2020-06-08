from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, PasswordField, validators, HiddenField

class RegistrationForm(FlaskForm):
    username = StringField('Имя', [validators.DataRequired()])
    email = StringField('e-mail')
    password = PasswordField('Пароль', [validators.DataRequired()])


class RemoveRecipe(FlaskForm):
    """
    remove recipe from favorite list
    """
    recipe = HiddenField()
