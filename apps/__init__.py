from flask import Flask

app = Flask(__name__)
#app.secret_key = '123456'
app.config.from_object('config')
from apps import views
