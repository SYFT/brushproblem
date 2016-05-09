# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, \
					SubmitField, FileField, TextAreaField, SelectField
from wtforms.validators import *
import datetime

# error message
ERROR_TOO_LONG = u'Too long !!'
ERROR_EMPTY = u'This field should not be empty!!'

class UserForm(Form) :
	username = StringField('username', 
				validators = [DataRequired(message = ERROR_EMPTY), 
					Length(max = 16, message = ERROR_TOO_LONG)])
	password = PasswordField('password', 
				validators = [DataRequired(message = ERROR_EMPTY), 
					Length(max = 16, message = ERROR_TOO_LONG)])
	submit = SubmitField(u'submit')

class LoginForm(UserForm):
	remember_me = BooleanField(u'remember_me', default = False)


class RegisterForm(UserForm) :
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

class EditForm(UserForm) :
	newPassword = PasswordField('password', 
				validators = [
					EqualTo('confirm', message = u'Passwords must match'), 
					Length(max = 16, message = ERROR_TOO_LONG)])
	confirm  = PasswordField('repeatPassword', 
				validators = [
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
	suggestion = TextAreaField('suggestion', 
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

class ChoiceForm(Form) :
	option = BooleanField('option', default = False)
	description = ""

class ProblemForm(Form) :
	pid = int
	index = int
	description = unicode
	choices = []
	# The return value is a list
	check = 0
	message = ''
	# 0 -> unSelect  1 -> Wrong  2 -> Right

class BrushForm(Form) :
	pro = []
	submit = SubmitField(u'submit')
	hideCorrectProblem = BooleanField('hideCorrectProblem', default = False)
	