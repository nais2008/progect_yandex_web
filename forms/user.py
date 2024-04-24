from flask_wtf import FlaskForm
from wtforms import PasswordField, EmailField, SubmitField, StringField, IntegerField, DateField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField('Ведите email:', validators=[DataRequired()])
    password = PasswordField('Введите пароль:', validators=[DataRequired()])
    submit = SubmitField('Авторизоваться')


class RegisterForm(FlaskForm):
    email = EmailField('Введите email:', validators=[DataRequired()])
    full_name = StringField('Введите ФИО:', validators=[DataRequired()])
    age = IntegerField('Введите возраст:', validators=[DataRequired()])
    birthday = DateField('Введите ДР:', validators=[DataRequired()])
    password = PasswordField('Пароль: ', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль: ', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class UpdateForm(FlaskForm):
    full_name = StringField('Введите ФИО:', validators=[DataRequired()])
    age = IntegerField('Введите возраст:', validators=[DataRequired()])
    birthday = DateField('Введите ДР:', validators=[DataRequired()])
    email = EmailField('Введите email:', validators=[DataRequired()])
    submit = SubmitField('Сохранить')


class CheckEmailForm(FlaskForm):
    email = EmailField('Введите email:', validators=[DataRequired()])
    submit = SubmitField('Проверить')


class ChangePasswordForm(FlaskForm):
    new_password = PasswordField('Введите новый пароль:', validators=[DataRequired()])
    new_password_again = PasswordField('Повторите новый пароль:', validators=[DataRequired()])
    submit = SubmitField('Сохранить')