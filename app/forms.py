import field as field
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError

from app.database_ops import get_coin_id_list_from_db


# Form class for the form on the home page i.e. to select coin for sentiment analysis.
class HomeForm(FlaskForm):
    coin = StringField('Please Choose a Coin Name: ', validators=[DataRequired()])
    submit = SubmitField('Analyse Tweets!')


# customised validation method to validate coin_id field of NewCoinForm form class.
def validate_coin_name(form, field):
    all_coins_from_db = get_coin_id_list_from_db()
    if field.data in all_coins_from_db:
        raise ValidationError('Coin Id already exist.')


# Form class for the form to add new coin in the data base
class NewCoinForm(FlaskForm):
    coin_id = StringField('Coin ID', validators=[DataRequired(), validate_coin_name])
    confirm_data = BooleanField('Confirm Data', validators=[DataRequired(), ])
    submit = SubmitField('Add')


# Form class to render Admin Login Form.
class AdminLoginForm(FlaskForm):
    name = StringField('Username: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    submit = SubmitField('Login')


# customised validation method to validate coin_id field NewTagForm form class.
def validate_coin_id(form, field):
    all_coins_id_from_db = get_coin_id_list_from_db()
    if field.data not in all_coins_id_from_db:
        raise ValidationError('Coin Id does not exist.')


# Form class to render New Tag Form
class NewTagForm(FlaskForm):
    coin_id = StringField('Coin Id', validators=[DataRequired(), validate_coin_id])
    coin_tag = StringField('Coin Tag', validators=[DataRequired()])
    submit = SubmitField('Add')


# Form class to render New Tag Form
class RemoveTagForm(FlaskForm):
    coin_id = StringField('Coin Id', validators=[DataRequired(), validate_coin_id])
    coin_tag = StringField('Coin Tag', validators=[DataRequired()])
    submit = SubmitField('Remove')


# Form class to render Delete Tag Form
class DeleteTagForm(FlaskForm):
    coin_id = StringField('Coin Id', validators=[DataRequired(), validate_coin_id])
    submit = SubmitField('Delete')




