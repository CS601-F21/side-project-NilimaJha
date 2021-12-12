import field as field
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError

from app.database_test import get_coin_id_list_from_db


# class LoginForm(FlaskForm):
#     accessname = StringField('Username', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     remember_me = BooleanField('Remember Me')
#     submit = SubmitField('Submit')


# Form class for the form on the home page i.e to select coin for sentiment analysis.
class HomeForm(FlaskForm):
    coin = StringField('Coin Name', validators=[DataRequired()])
    submit = SubmitField('submit')


# customised validation method to validate coin_id field of NewCoinForm form class.
def validate_coin_name(form, field):
    all_coins_from_db = get_coin_id_list_from_db()
    if field.data in all_coins_from_db:
        raise ValidationError('Coin Id already exist.')


# Form class for the form to add new coin in the data base
class NewCoinForm(FlaskForm):
    coin_name = StringField('Coin Name', validators=[DataRequired()])
    coin_id = StringField('Coin ID', validators=[DataRequired(), validate_coin_name])
    coin_symbol = StringField('Coin Symbol', validators=[DataRequired()])
    confirm_data = BooleanField('Confirm Data', validators=[DataRequired(), ])
    submit = SubmitField('Add')


class AdminLoginForm(FlaskForm):
    name = StringField('Login As', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


