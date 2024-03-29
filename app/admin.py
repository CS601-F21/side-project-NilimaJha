from urllib import request

from app import app
from app.database_ops import insert_into_crypto_coins_table, process_insert_tag, validate_tag_for_coin_id, \
    process_delete_tag, process_delete_coin
from flask import render_template, redirect, url_for, request, flash
from app.forms import AdminLoginForm, NewCoinForm, NewTagForm, RemoveTagForm, DeleteTagForm
from config import Config

import requests


# method to handle GET and POST request for admin login
# This feature is not implemented yet.
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        app.logger.debug(request.form['name'])
        return redirect(url_for('add_new_coin', admin=request.form['name'], password=request.form['password']))
    return render_template('login.html', title='Admin Login', form=form)


# method to handle GET and POST request to add_new_coin request by the user.
@app.route('/add_new_coin/<admin>/<password>', methods=['GET', 'POST'])
def add_new_coin(admin, password):
    form = NewCoinForm()
    if form.validate_on_submit():
        app.logger.debug("Got a submit.")
        app.logger.debug(request.form)
        get_coin_by_id_url = "https://api.coingecko.com/api/v3/coins/{}?localization=en&tickers=false&community_data=false"\
            .format(request.form['coin_id'])

        response = requests.request("GET", get_coin_by_id_url)
        app.logger.debug(response.status_code)
        if response.status_code != 200:
            app.logger.debug("ERROR : COIN ID: {} -> Details not available on CoinGecko"
                  .format(request.form['coin_id']))
            app.logger.debug("ERROR : response.status_code : {} \n -> response.text: {}"
                  .format(response.status_code, response.text))
            # raise Exception(response.status_code, response.text)
            flash("ALERT: Invalid Coin! \"{}\" Details Couldn't be collected from CoinGecko API".format(request.form['coin_id']))
            return redirect(url_for('add_new_coin', admin=admin, password=password))

        response_data = response.json()
        app.logger.debug(">> coin_id     : " + str(response_data['id']))
        app.logger.debug(">> coin_symbol : " + str(response_data['symbol']))
        app.logger.debug(">> coin_name   : " + str(response_data['name']))

        # and return success page.
        coin_inserted = insert_into_crypto_coins_table(coin_id=response_data['id'],
                                                       coin_name=response_data['name'],
                                                       coin_symbol=response_data['symbol'])
        if coin_inserted:
            flash("INFO: {} is successfully added to your list".format(response_data['id']))
            return redirect(url_for('add_new_coin', admin=admin, password=password))
        else:
            flash("ALERT: Failed to Enter Data into DB")
            return redirect(url_for('add_new_coin', admin=admin, password=password))

    if admin == Config.ADMIN_LOGIN_NAME and password == Config.ADMIN_LOGIN_PASSWORD:
        return render_template('add_new_coin.html', title='Add New Coin', form=form)
    else:
        flash("ALERT: Invalid Login Credentials.")
        return redirect(url_for('admin_login'))


# method to handle GET and POST request to add new tags for a coin in the database
@app.route('/add_new_tag', methods=['GET', 'POST'])
def add_new_tag():
    form = NewTagForm()
    if form.validate_on_submit():
        app.logger.debug("Got a submit.")
        app.logger.debug(request.form)
        tag_insertion = process_insert_tag(request.form['coin_id'], request.form['coin_tag'])
        if tag_insertion:
            app.logger.debug('insertion successful page')
            return render_template('new_tag_added.html',
                                   title='New Tag Added',
                                   coin_id=request.form['coin_id'],
                                   coin_tag=request.form['coin_tag'])
        else:
            app.logger.debug('tag entered already exist')
            return render_template('tag_already_exist.html',
                                   title='Tag Already Exist',
                                   coin_id=request.form['coin_id'],
                                   coin_tag=request.form['coin_tag'])
    return render_template('add_new_tag.html', title='Add New Tag', form=form)


# method to handle GET and POST request for remove tag by the user.
@app.route('/remove_tag', methods=['GET', 'POST'])
def remove_tag():
    form = RemoveTagForm()
    if form.validate_on_submit():
        tag_delete = process_delete_tag(request.form['coin_id'], request.form['coin_tag'])
        if tag_delete:
            return render_template('tag_removed.html',
                                   title='Tag Removed',
                                   coin_id=request.form['coin_id'],
                                   coin_tag=request.form['coin_tag'])
        else:
            return render_template('tag_removal_unsuccessful.html',
                                   title='Tag Does not Exist',
                                   coin_id=request.form['coin_id'],
                                   coin_tag=request.form['coin_tag'])
    return render_template('remove_tag.html', title='Remove Tag', form=form)


# method to handle GET and POST request for deleting coin from the db.
@app.route('/delete_coin', methods=['GET', 'POST'])
def delete_coin():
    form = DeleteTagForm()
    if form.validate_on_submit():
        process_delete_coin(request.form['coin_id'])
        return render_template('coin_removed.html',
                               title='Coin Removed',
                               coin_id=request.form['coin_id'])

    return render_template('delete_coin.html', title='Delete Coin', form=form)


