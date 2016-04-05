from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
#app.secret_key = '123456'
app.config.from_object('config')
db = SQLAlchemy(app)
from apps import views, models
