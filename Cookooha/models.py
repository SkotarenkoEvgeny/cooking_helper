from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

ingredients_recipes_association = db.Table(
    "ingredients_recipes",
    db.Column("ingredient_id", db.Integer, db.ForeignKey("ingredients.id")),
    db.Column("recipe_id", db.Integer, db.ForeignKey("recipes.id")))


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    username = db.Column(db.String())
    email = db.Column(db.String())
    password_hash = db.Column(db.String())
    recipe = db.relationship("Recipe")

    @property
    def password(self):
        print('hash from bd', self.password_hash)
        raise AttributeError("Вам не нужно знать пароль!")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def password_valid(self, password):
        return check_password_hash(self.password_hash, password)


class Ingredient_Group(db.Model):
    __tablename__ = "ingredient_groups"
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String())


class Ingredient(db.Model):
    __tablename__ = "ingredients"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    title = db.Column(db.String())
    ingredient_group = db.Column(db.Integer())
    recipe = db.relationship("Recipe", secondary=ingredients_recipes_association, back_populates="ingredient")


class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    title = db.Column(db.String())
    picture = db.Column(db.String())
    description = db.Column(db.String())
    time = db.Column(db.Integer())
    servings = db.Column(db.Integer())
    kcal = db.Column(db.Integer())
    instruction = db.Column(db.String())
    ingredient = db.relationship("Ingredient", secondary=ingredients_recipes_association, back_populates="recipe")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User")
