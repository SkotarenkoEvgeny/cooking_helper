import random

from flask import Flask, render_template, session, redirect, request, abort
from models import User, Ingredient, Ingredient_Group, Recipe, db
from forms import RegistrationForm, RemoveRecipeForm, ProductForm

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cook_db.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route('/')
def home():
    user = User.query.get(session.get('user_id', None))
    random_recipe_list = random.sample(Recipe.query.all(), 6)
    return render_template('index.html', random_recipe_list=random_recipe_list, user=user)


@app.route('/recipes/')
def recipes():
    user = User.query.get(session.get('user_id', None))
    return render_template('recipes.html', user=user)


@app.route('/favorites_add/<int:recipe_id>/')
def favorites_worker(recipe_id):
    if session.get("user_id"):
        user = User.query.get(session.get("user_id"))
        recipe = Recipe.query.get(recipe_id)
        user.recipe.append(recipe)
        session['recipe_condition'] = 'add'
        db.session.add(user)
        db.session.commit()
        return redirect('/favorites/')
    return redirect('/registration/')


@app.route('/favorites/')
def favorites():
    if session.get("user_id"):
        user = User.query.get(session.get("user_id"))
        form = RemoveRecipeForm()
        recipe_condition = session.get('recipe_condition', None)
        if recipe_condition is not None:
            session['recipe_condition'] = None
        return render_template('fav.html', fav_recipes=user.recipe, form=form, recipe_condition=recipe_condition,
                               user=user)


@app.route('/favorites_remove/', methods=["POST"])
def remove_favorites():
    form = RemoveRecipeForm(request.form)
    recipe_id = int(form.recipe.data)
    if session.get("user_id"):
        user = User.query.get(session.get("user_id"))
        recipe = Recipe.query.get(recipe_id)
        user.recipe.remove(recipe)
        session['recipe_condition'] = 'del'
        db.session.add(user)
        db.session.commit()
        return redirect('/favorites/')


@app.route('/recipe/<int:recipe_id>/')
def recipe(recipe_id):
    recipe_unit = Recipe.query.get(recipe_id)
    user = User.query.get(session.get('user_id', None))
    if recipe_unit is None:
        abort(404)
    return render_template('recipe.html', recipe=recipe_unit, user=user)


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


@app.route('/list/')
def list():
    rez_dict = {}
    for item in Ingredient_Group.query.all():
        product_list = ProductForm(Ingredient.query.filter(Ingredient.ingredient_group == item.id).all())

        print([i.title for i in Ingredient.query.filter(Ingredient.ingredient_group == item.id).all()])
        print(product_list.__dict__)
        rez_dict[item.title] = product_list

    # for item in Ingredient_Group.query.all():
    #     product_list = [ProductForm(name=i.title, id=i.id) for i in
    #                     Ingredient.query.filter(Ingredient.ingredient_group == item.id).all()]
    #     print([i.title for i in Ingredient.query.filter(Ingredient.ingredient_group == item.id).all()])
    #     print([i.product.name for i in product_list][0])
    #     rez_dict[item.title] = product_list
    # print(rez_dict)
    return render_template('list.html', rez_dict=rez_dict)


if __name__ == "__main__":
    app.run()
