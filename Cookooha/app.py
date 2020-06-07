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


@app.route('/')
def home():
    user = User.query.get(session.get('user_id', None))
    print(session)
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
    return render_template('recipe.html', recipe=recipe_unit)


@app.route('/registration/', methods=["GET", "POST"])
def registration():
    if session.get("user_id"):
        return redirect("/")
    form = RegistrationForm(request.form)
    if request.method == "POST":
        users_list = User.query.filter(User.username == form.username.data).all()
        if len(users_list) != 0:
            for item in users_list:
                if item.password_valid(form.password.data):
                    session['user_id'] = item.id
            return redirect("/")

        elif form.validate_on_submit():
            user = User()
            user.username = form.username.data
            user.password = form.password.data
            if form.email.data:
                user.email = form.email.data
                db.session.add(user)
                db.session.commit()
                session['user_id'] = User.query.get(user.username == user.username).id
                return redirect("/")
            else:
                form.email.errors.append("Введите E-mail")
    return render_template("login.html", form=form)


@app.route('/logout/')
def logout():
    session.pop("user_id")
    return redirect('/')


if __name__ == "__main__":
    app.run()
