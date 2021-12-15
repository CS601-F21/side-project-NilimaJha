from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)

from app import models, home, routes, data_analysis_ops, database_ops, admin


# def __main__():
#     print("*" * 80)
#     if 'abc' == 'Abc':
#         print("True")
#     else:
#         print("False")
#
#     print("*" * 80)
#
# print("+" * 80)
# __main__()
# print("+" * 80)
