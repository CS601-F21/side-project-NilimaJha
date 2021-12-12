from urllib import request

from app import app
from app.database_ops import insert_into_crypto_coins_table
from flask import render_template, redirect, url_for, request
from app.forms import AdminLoginForm, NewCoinForm
from config import Config

import requests
import json

@app.route('/add_new_coin', methods=['GET', 'POST'])
def add_new_coin_form():
    form = AdminLoginForm()
    if form.validate_on_submit():
        print(request.form['name'])
        return redirect(url_for('add_new_coin', admin=request.form['name'], password=request.form['password']))
    return render_template('login.html', title='Add New Coin', form=form)


@app.route('/add_new_coin/<admin>/<password>', methods=['GET', 'POST'])
def add_new_coin(admin, password):
    form = NewCoinForm()
    if form.validate_on_submit():
        print("Got a submit.")
        print(request.form)
        # print(request.form['coin_id'])
        # print(request.form['confirm_data'])
        # validate data , check if the data already exist in db if yes return invalid data else add in db

        get_coin_by_id_url = "https://api.coingecko.com/api/v3/coins/{}?localization=en&tickers=false&community_data=false"\
            .format(request.form['coin_id'])

        response = requests.request("GET", get_coin_by_id_url)
        print("~~~~~~~~~~~~~~~")
        print(response.status_code)
        if response.status_code != 200:
            print("ERROR : COIN ID: {} -> Details not available on CoinGecko"
                  .format(request.form['coin_id']))
            print("ERROR : response.status_code : {} \n -> response.text: {}"
                  .format(response.status_code, response.text))
            # raise Exception(response.status_code, response.text)
            return render_template('invalid_coin.html')

        response_data = response.json()
        print(">> coin_id     : " + str(response_data['id']))
        print(">> coin_symbol : " + str(response_data['symbol']))
        print(">> coin_name   : " + str(response_data['name']))

        # and return success page.
        coin_inserted = insert_into_crypto_coins_table(coin_id=response_data['id'],
                                                       coin_name=response_data['name'],
                                                       coin_symbol=response_data['symbol'])
        if coin_inserted:
            return render_template('Successful.html')
        else:
            print("ERROR : Failed to Enter Data into DB")
            # get_data_from_crypto_currency()
            return "False"
    if admin == Config.ADMIN_LOGIN_NAME and password == Config.ADMIN_LOGIN_PASSWORD:
        return render_template('add_new_coin.html', title='Add New Coin', form=form)
    else:
        return render_template('not_Authorized.html')
