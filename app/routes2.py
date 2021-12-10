from flask import render_template, flash, redirect, url_for
from app import app
from app.form import LoginForm
from app.form import HomeForm
from flask import Flask
from requests_oauthlib.oauth1_auth import Client


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/home', methods=['GET', 'POST'])
def home():
    form = HomeForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('home.html', title='Home', form=form)

