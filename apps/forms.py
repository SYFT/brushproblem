from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField
from wtforms.validators import *

# error message
ERROR_TOO_LONG = u'Too long !!'
ERROR_EMPTY = u'This field should not be empty!!'

class LoginForm(Form):
	username = StringField('username', validators = [DataRequired(message = ERROR_EMPTY), Length(max = 16, message = ERROR_TOO_LONG)])
	password = PasswordField('password', validators = [DataRequired(message = ERROR_EMPTY), Length(max = 16, message = ERROR_TOO_LONG)])
	remember_me = BooleanField(u'remember_me', default = False)
	submit = SubmitField(u'submit')


class RegisterForm(LoginForm) :
	password = PasswordField('password', validators = [DataRequired(message = ERROR_EMPTY), EqualTo('confirm', message = u'Passwords must match'), Length(max = 16, message = ERROR_TOO_LONG)])
	confirm  = PasswordField('repeatPassword', validators = [DataRequired(message = ERROR_EMPTY), Length(max = 16)])
	email = StringField('emailaddress', validators = [DataRequired(message = ERROR_EMPTY), Length(max = 64, message = ERROR_TOO_LONG), Email(message = u'Is this a email address ?')])

class UploadForm() :
	file = FileField('file', validators = [DataRequired()])
	submit = SubmitField(u'submit')
