from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from requests_oauthlib.oauth1_auth import Client
# from flask_restful import Api
# import tweepy


app = Flask(__name__)
app.debug = True
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import routes, routes2, models


# def __main__():
#     print("*" * 80)
#     print("in main")
#
#     print("*" * 80)
#
# print("+" * 80)
# __main__()
# print("+" * 80)
