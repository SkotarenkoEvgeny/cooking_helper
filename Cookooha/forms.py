from flask_wtf import FlaskForm
from wtforms import Form, RadioField, StringField, PasswordField, validators, HiddenField, FieldList, FormField
from models import Ingredient

class RegistrationForm(FlaskForm):
    username = StringField('Имя', [validators.DataRequired()])
    email = StringField('e-mail')
    password = PasswordField('Пароль', [validators.DataRequired()])


class RemoveRecipeForm(FlaskForm):
    """
    remove recipe from favorite list
    """
    recipe = HiddenField()


class ProductForm(FlaskForm):
    pass



# class ProductListForm(FlaskForm):
#     product_list = FieldList(FormField(ProductForm), min_entries=1)
