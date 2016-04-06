from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import *

class LoginForm(Form):
	username = StringField(u'username', validators = [DataRequired()])
	password = StringField(u'password')
	remember_me = BooleanField(u'remember_me', default = False)
	