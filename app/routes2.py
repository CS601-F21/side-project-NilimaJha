from urllib import request

from flask import render_template, flash, redirect, url_for, request
from app import app
from app.form import LoginForm, NewCoinForm, AdminLoginForm
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
from config import Config


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


