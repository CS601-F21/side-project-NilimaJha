from urllib import request
from flask import render_template, flash, redirect, url_for, request
from app import app
from app.database_test import get_coin_name_list_from_db
from app.forms import HomeForm


@app.route('/home1', methods=['GET', 'POST'])
def print11():
    form = HomeForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('home.html', title='Home', form=form)


@app.route('/home', methods=['GET', 'POST'])
def home():
    form = HomeForm()
    coin_name_list = get_coin_name_list_from_db()
    # coin_name_list = ['a', 'bbbbb', 'cccccccccccccccc', 'ddddddddddddddxddddddddddddddd']
    # print(coin_name_list)
    if form.validate_on_submit():
        data = request.form['coin']
        # print(data)
        return redirect(url_for('get_tweets_from_twitter', coin_name=data))
        # return 'index.html'
    return render_template('home.html', title='Home Trying Drop-Down', coin_name_list=coin_name_list, form=form)


