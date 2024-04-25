from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, FileField, SelectField, IntegerField
from wtforms.validators import DataRequired
import sqlite3

try:
    conn = sqlite3.connect('db/gs.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM product_category")
    items = cur.fetchall()
except:
    items = [("1", "Ничего не найденно ")]


class ProductForm(FlaskForm):
    name = StringField('Название: ', validators=[DataRequired()])
    price = IntegerField('Цена: ', validators=[DataRequired()])
    description = TextAreaField('Описание: ', validators=[DataRequired()])
    category = SelectField(
        u'Категория: ',
        choices=[
            (f"{item[0]}", f"{item[1]}") for item in items
        ]
    )
    image1 = FileField('Изображение 1')
    image2 = FileField('Изображение 2')
    submit = SubmitField('Создать')


class UpdateProductForm(FlaskForm):
    name = StringField('Название: ', validators=[DataRequired()])
    price = IntegerField('Цена: ', validators=[DataRequired()])
    description = TextAreaField('Описание: ', validators=[DataRequired()])
    category = SelectField(
        u'Категория: ',
        choices=[
            (f"{item[0]}", f"{item[1]}") for item in items
        ]
    )
    submit = SubmitField('Редактировать')