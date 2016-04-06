from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import baseDir

app = Flask(__name__)
#app.secret_key = '123456'
app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
openID = OpenID(app, os.path.join(baseDir, 'tmp'))

from apps import views, models
reload(sys)
sys.setdefaultencoding('utf8')
text_factory = str