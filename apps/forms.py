# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, \
					SubmitField, FileField, TextAreaField, SelectField, \
					SelectMultipleField
from wtforms.validators import *
import datetime

# error message
ERROR_TOO_LONG = u'Too long !!'
ERROR_EMPTY = u'This field should not be empty!!'

class LoginForm(Form):
	username = StringField('username', 
				validators = [DataRequired(message = ERROR_EMPTY), 
					Length(max = 16, message = ERROR_TOO_LONG)])
	password = PasswordField('password', 
						validators = [DataRequired(message = ERROR_EMPTY), 
							Length(max = 16, message = ERROR_TOO_LONG)])
	remember_me = BooleanField(u'remember_me', default = False)
	submit = SubmitField(u'submit')


class RegisterForm(LoginForm) :
	password = PasswordField('password', 
				validators = [DataRequired(message = ERROR_EMPTY), 
					EqualTo('confirm', message = u'Passwords must match'), 
					Length(max = 16, message = ERROR_TOO_LONG)])
	confirm  = PasswordField('repeatPassword', 
				validators = [DataRequired(message = ERROR_EMPTY), 
					Length(max = 16, message = ERROR_TOO_LONG)])
	email = StringField('emailaddress', 
				validators = [DataRequired(message = ERROR_EMPTY), 
					Length(max = 64, message = ERROR_TOO_LONG), 
					Email(message = u'Is this a email address ?')])

class UploadForm(Form) :
	file = TextAreaField('file', 
				validators = [DataRequired(message = ERROR_EMPTY)])
	filename = StringField('filename', 
				validators = [DataRequired(message = ERROR_EMPTY), 
					Length(min = 2, max = 16, 
						message = u'Length should between 2 and 16!!')])
	submit = SubmitField(u'submit')
	subject = SelectField('subject', coerce = int, 
		validators = [DataRequired(message = ERROR_EMPTY)])

class SuggestionForm(Form) :
	suggestion = TextAreaField('suggestion', _name = 'suggestion', 
		validators = [DataRequired(message = ERROR_EMPTY), 
			Length(max = 64, message = ERROR_TOO_LONG)])
	submit = SubmitField(u'submit')

class SearchProblemForm(Form) :
	subject = SelectField('subject', coerce = int, 
				validators = [DataRequired(message = ERROR_EMPTY)])
	filename = StringField('filename', 
				validators = [DataRequired(message = ERROR_EMPTY), 
					Length(min = 2, max = 16, 
						message = u'Length should between 2 and 16!!')])
	timeDelta = SelectField('timedelta', 
					validators = [DataRequired(message = ERROR_EMPTY)], 
					coerce = int)
	submit = SubmitField(u'submit')
							
# SelectField->coerce is the return type, which is the first part of choices
	
class ProblemForm(Form) :
	pid = int
	index = int
	description = unicode
	choice = SelectMultipleField('choice')
	# The return value is a list
	check = 0
	message = ''
	# 0 -> unSelect  1 -> Wrong  2 -> Right

class BrushForm(Form) :
	pro = []
	submit = SubmitField(u'submit')
	