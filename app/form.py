from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    accessname = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Submit')


class HomeForm(FlaskForm):
    coin = StringField('Coin Name', validators=[DataRequired()])
    submit = SubmitField('submit')


class NewCoinForm(FlaskForm):
    coin_name = StringField('Coin Name', validators=[DataRequired()])
    coin_id = StringField('Coin ID', validators=[DataRequired()])
    coin_symbol = StringField('Coin Symbol', validators=[DataRequired()])
    confirm_data = BooleanField('Confirm Data', validators=[DataRequired(), ])
    submit = SubmitField('Add')


class AdminLogin(FlaskForm):
    name = StringField('Login As', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')
