import json

from app import app
from models import Ingredient, Ingredient_Group, Recipe, db

app.app_context().push()
db.init_app(app)
db.create_all()

with open("ingredient_groups.json", "r") as f:
    ingredient_groups = json.load(f)

for item in ingredient_groups:
    unit = Ingredient_Group(id=item['id'], title=item['title'])
    db.session.add(unit)

with open("ingredients.json", "r") as f:
    ingredients = json.load(f)

for item in ingredients:
    unit = Ingredient(id=item['id'], title=item["title"], ingredient_group=item["ingredient_group"])
    db.session.add(unit)

with open("recipes.json", "r") as f:
    recipes = json.load(f)

for item in recipes:
    unit = Recipe()
    unit.title = item["title"]
    unit.picture = item["picture"]
    unit.description = item["description"]
    unit.time = item["time"]
    unit.servings = item["servings"]
    unit.kcal = item["kcal"]
    unit.instruction = item["instruction"]
    for i in item["ingredients"]:
        element = Ingredient.query.get(i)
        unit.ingredient.append(element)

db.session.commit()
