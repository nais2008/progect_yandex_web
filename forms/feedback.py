from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class FeedbackForm(FlaskForm):
    text = TextAreaField("Введите отзыв: ", validators=[DataRequired()])
    submit = SubmitField('Оставить отзыв')