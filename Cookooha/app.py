import random

from flask import Flask, render_template, abort, session, redirect, request
from models import User, Ingredient, Ingredient_Group, Recipe, db
from forms import RegistrationForm

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cook_db.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.route('/') # complete
def home():
    user = session.get('user_id', None)
    random_recipe_list = random.sample(Recipe.query.all(), 6)
    return render_template('index.html', random_recipe_list=random_recipe_list, user=user)


@app.route('/recipes/')
def recipes():
    return render_template('recipes.html')


@app.route('/recipe/<int:recipe_id>/')
def recipe(recipe_id):
    recipe_unit = Recipe.query.get(recipe_id)
    if recipe_unit is None:
        abort(404)
    print(recipe_unit.ingredient)
    return render_template('recipe.html', recipe=recipe_unit)

@app.route('/registration/', methods=["GET", "POST"])
def registration():
    if session.get("user_id"):
        return redirect("/")
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        session['user_id'] = User.query.get(user.username==user.username).id
        print('user')
        return render_template("login.html", form=form)

    return render_template("login.html", form=form)



@app.route('/login/')
def login():

    return render_template('login.html')


@app.route('/logout/')
def logout():

    return render_template('login.html')


if __name__ == "__main__":
    app.run()
