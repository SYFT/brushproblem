# -*- coding: utf-8 -*-

from flask import Flask, g, url_for
from flask.ext.sqlalchemy import SQLAlchemy
import os, sys
from flask.ext.login import LoginManager
from werkzeug import secure_filename


APP_NAME = __name__
app = Flask(APP_NAME)
#app.secret_key = '123456'
app.config.from_object('config')


# create database
db = SQLAlchemy(app)
from .models import *




import flask.ext.whooshalchemy
# 每个希望可以被检索的表都要被whoosh_index
flask.ext.whooshalchemy.whoosh_index(app, User)
flask.ext.whooshalchemy.whoosh_index(app, Document)





ADMIN_NAME = 'MyAdmin'
admin = Admin(name = ADMIN_NAME)
admin.init_app(app)
admin.add_view(MyView(name = 'Hello'))
admin.add_view(MyModelView(User, db.session, name = u'用户', category = u'管理'))
admin.add_view(MyModelView(Document, db.session, name = u'试卷', category = u'管理'))
admin.add_view(MyModelView(Problem, db.session, name = u'具体题目', category = u'管理'))
admin.add_view(MyModelView(Subject, db.session, name = u'科目', category = u'管理'))






LOGIN_MESSAGE = u'Please login first.'
# flash while access some login_required pages
# without login
REFRESH_MESSAGE = (u"To protect your account, please reauthenticate to access this page.")
# a list of message that will flash while 
# a non-fresh user access some fresh_login_required
# pages (it means the user can not login by cookies)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
lm.login_message = LOGIN_MESSAGE
lm.refresh_view = 'login'
lm.needs_refresh_message = REFRESH_MESSAGE

@lm.user_loader
def load_user(id) :
	return User.query.get(int(id))



from flask.ext.uploads import UploadSet, \
							patch_request_class, \
							configure_uploads
us = UploadSet('us', extensions = app.config['ALLOWED_EXTENSIONS'])
configure_uploads(app, (us, ))
patch_request_class(app, size = app.config['MAX_CONTENT_LENGTH'])

	
	
	


from apps.views import frontend, loginpages, registerpages, uploadpages, \
						viewproblems
MODULES = (
(frontend, ''),
(loginpages, ''),
(registerpages, ''),
(uploadpages, ''),
(viewproblems, '')
)
# the first parameter is the module's name
# the second parameter is the url_prefix of the module

# register blueprint modules
for module, url_prefix in MODULES :
	app.register_blueprint(module, url_prefix = url_prefix)





# set default language
# 'str' or 'unicode' or 
# 'optimized unicode' or 'custom functon'
reload(sys)
sys.setdefaultencoding('utf-8')
text_factory = str
