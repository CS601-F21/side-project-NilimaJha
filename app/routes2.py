from urllib import request

from flask import render_template, flash, redirect, url_for, request
from app import app
from app.database_test import insert_into_crypto_coins_table
from app.form import LoginForm, NewCoinForm, AdminLogin, AdminLoginForm
from app.form import HomeForm


# @app.route('/users_post')
# def users_post():
#     user = {'username': 'Nilima Jha'}
#     posts = [
#         {
#             'author': {'username': 'Nitya'},
#             'body': 'Beautiful day in Delhi!'
#         },
#         {
#             'author': {'username': 'Nidhi'},
#             'body': 'The Avengers movie was so cool!'
#         },
#         {
#             'author': {'username': 'Amish'},
#             'body': 'Reading Book helps!'
#         },
#         {
#             'author': {'username': 'Anant'},
#             'body': 'Really excited for Spider Man! No Way Home!'
#         },
#         {
#             'author': {'username': 'Joy'},
#             'body': 'Marry Christmas everyone!'
#         },
#         {
#             'author': {'username': 'Jyoti'},
#             'body': 'In Kathmandu, Having Fun!'
#         },
#         {
#             'author': {'username': 'Kirti'},
#             'body': 'Really Excited for 2022!'
#         },
#         {
#             'author': {'username': 'Rohit'},
#             'body': 'Really excited for Money Hiest!'
#         }
#     ]
#     return render_template('users_post.html', user=user, posts=posts)


@app.route('/listlog', methods=['GET', 'POST'])
def login1():
    form = LoginForm()
    # get data from db make alist of it and then send it to the form.
    namelist = ['a', 'b', 'c', 'd']
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form, namelist=namelist)


@app.route('/home1', methods=['GET', 'POST'])
def home1():
    form = HomeForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('home.html', title='Home', form=form)


@app.route('/printname', methods=['GET', 'POST'])
def printingList():
    form = HomeForm()
    coin_name_list = ['a', 'bbbbb', 'cccccccccccccccc', 'ddddddddddddddxddddddddddddddd']
    print(coin_name_list)
    if form.validate_on_submit():
        data = request.form['coin']
        print(data)
        return 'index.html'
    return render_template('home.html', title='Home Trying Drop-Down', coin_name_list=coin_name_list, form=form)


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
    if admin == '@dm!n' and password == "p@ssw0rd":
        return render_template('add_new_coin.html', title='Add New Coin', form=form)
    else:
        return render_template('not_Authorized.html')
