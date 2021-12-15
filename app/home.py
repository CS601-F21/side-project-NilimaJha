from urllib import request
from flask import render_template, flash, redirect, url_for, request
from app import app
from app.database_ops import get_coin_name_list_from_db
from app.forms import HomeForm
import app.data_analysis_ops as da_ops


@app.route('/home', methods=['GET', 'POST'])
def home():
    form = HomeForm()
    coin_name_list = get_coin_name_list_from_db()

    if form.validate_on_submit():
        data = request.form['coin']
        return redirect(url_for('get_tweets_from_twitter', coin_name=data))

    top_searched_coins = da_ops.top_trending_searched_coins()
    if len(top_searched_coins) == 0:
        flash("ALERT:  Top Trending Searched Coins details Couldn't be collected from CoinGecko API")

    return render_template('home.html', title='Home Page', coin_name_list=coin_name_list, form=form, top_searched_coins=top_searched_coins)




