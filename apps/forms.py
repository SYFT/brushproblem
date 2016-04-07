from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import *

class LoginForm(Form):
	username = StringField(u'username', validators = [DataRequired(), Length(max = 16, message = u'Too long!')])
	password = PasswordField(u'password', validators = [DataRequired(), EqualTo(u'repeatedPassword', message = u'Password must match'), Length(max = 16, message = 'Too long')])
	repeatedPassword = PasswordField(u'rpassword', validators = [Length(max = 16)])
	remember_me = BooleanField(u'remember_me', default = False)
	