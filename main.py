from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, ForeignKey
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, URL
from datetime import date

from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
bootstrap = Bootstrap5()


#CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

#CONFIGURE TABLE

class GroceryList:
    pass


class Recipes(db.Model):
    __tablename__ = 'recipes'
    id = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    image_url: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String, nullable=False)
    ingredients: Mapped[str] = mapped_column(String, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer)
    instructions: Mapped[str] = mapped_column(String, nullable=False)


with app.app_context():
    db.create_all()


# WTForm
class CreateRecipeForm(FlaskForm):
    name = StringField("Recipe name", validators=[DataRequired()])
    image_url = StringField("Image URL", validators=[DataRequired()])
    description = StringField("YDescription", validators=[DataRequired()])
    ingredients = StringField("Ingredients", validators=[DataRequired(), URL()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    unit = StringField('Unit', validators=[DataRequired()])
    submit = SubmitField("Add recipe")




@app.route('/')
def index():
    #it's returning all recipes
    result = db.session.execute(db.select(Recipes))
    recipes = result.scalars().all()
    return render_template('index.html', recipes=recipes)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == 'POST':
        name = request.form['name'],
        image_url = request.form['image_url'],
        description = request.form['description'],
        ingredients = request.form['ingredients'],
        quantity = request.form['quantity']
        unit = request.form['unit']
        new_recipe = Recipes(name=name,
                             image_url=image_url,
                             description=description,
                             ingredients=ingredients,
                             quantity=quantity,
                             unit=unit,
                             )

        db.session.add(new_recipe)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("add.html")

if __name__ == '__main__':
    app.run(debug=True)