import os
from urllib import request
from flask import render_template, flash, redirect, url_for, request
from app import app
from app.database_ops import get_coin_name_list_from_db
from app.forms import HomeForm
import app.data_analysis_ops as da_ops
import logging


@app.before_first_request
def before_first_request():
    log_level = logging.DEBUG

    for handler in app.logger.handlers:
        app.logger.removeHandler(handler)

    root = os.path.dirname(os.path.abspath(__file__))
    logdir = os.path.join(root, 'logs')
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    log_file = os.path.join(logdir, 'crypto_app.log')
    default_formatter = logging.Formatter('%(asctime)s [%(levelname)s] : %(module)s - %(message)s')
    handler = logging.FileHandler(log_file)
    handler.setLevel(log_level)
    handler.setFormatter(default_formatter)
    app.logger.addHandler(handler)

    app.logger.setLevel(log_level)


# method to handle GET or POST request path /home
@app.route('/home', methods=['GET', 'POST'])
def home():
    app.logger.debug("In Home route.")
    form = HomeForm()
    coin_name_list = get_coin_name_list_from_db()

    # validating the data provided by the user.
    if form.validate_on_submit():
        data = request.form['coin']
        return redirect(url_for('get_tweets_from_twitter', coin_name=data))

    # getting top searched coins on CoinGeko.
    top_searched_coins = da_ops.top_trending_searched_coins()
    if len(top_searched_coins) == 0:
        flash("ALERT:  Top Trending Searched Coins details Couldn't be collected from CoinGecko API")

    return render_template('home.html', title='Home Page',
                           coin_name_list=coin_name_list,
                           form=form,
                           top_searched_coins=top_searched_coins)




