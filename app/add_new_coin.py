from urllib import request
from app import app
from app.database_test import insert_into_crypto_coins_table
from flask import render_template, redirect, url_for, request
from app.form import AdminLoginForm, NewCoinForm
from config import Config


@app.route('/add_new_coin', methods=['GET', 'POST'])
def add_new_coin_form():
    form = AdminLoginForm()
    if form.validate_on_submit():
        print(request.form['name'])
        return redirect(url_for('add_new_coin', admin=request.form['name'], password=request.form['password']))
    return render_template('login.html', title='Add New Coin', form=form)


@app.route('/add_new_coin/<admin>/<password>')
def add_new_coin(admin, password):
    form = NewCoinForm()
    if form.validate_on_submit():
        print("Got a submit.")
        print(request.form['coin_name'])
        print(request.form['coin_id'])
        print(request.form['confirm_data'])
        # validate data , check if the data already exist in db if yes return invalid data else add in db
        # and return success page.
        insert_into_crypto_coins_table(coin_id=request.form['coin_id'], coin_name=request.form['coin_name'], coin_symbol=request.form['coin_symbol'])
        return render_template('Successful.html')
    if admin == Config.ADMIN_LOGIN_NAME and password == Config.ADMIN_LOGIN_PASSWORD:
        return render_template('add_new_coin.html', title='Add New Coin', form=form)
    else:
        return render_template('not_Authorized.html')
