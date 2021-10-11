from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, SelectField, PasswordField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField

categories = [('Appetizer', 'Appetizer'), ('Soup', 'Soup'), ('Pizza', 'Pizza'),
              ('Pasta', 'Pasta'), ('Rice', 'Rice'), ('Coffee', 'Coffee'),
              ('Wine', 'Wine'), ('Dessert', 'Dessert'),
              ('Beverage', 'Beverage')]


class AddItemForm(FlaskForm):
    name = StringField('Item Name', validators=[DataRequired()])
    category = SelectField('Category',
                           choices=categories,
                           default=categories[0])
    description = StringField('Description', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    submit = SubmitField('Add Item')


class EditItemForm(FlaskForm):
    name = StringField('Item Name', validators=[DataRequired()])
    category = SelectField('Category',
                           choices=categories,
                           default=categories[0])
    description = StringField('Description', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    submit = SubmitField('Edit Item')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')


class DateForm(FlaskForm):
    selected_date = DateField(label='Date',
                              format='%Y-%m-%d',
                              default=date.today(),
                              validators=[DataRequired()])
    submit = SubmitField('Select date')