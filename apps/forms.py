# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, \
					SubmitField, FileField, TextAreaField, SelectField
from wtforms.validators import *
import datetime

# error message

def ERROR_EMPTY(name) :
	return unicode(name) + u'不能为空！'

def ERROR_LENGTH(name, min = None, max = None) :
	ret = u'你输入的' + unicode(name) + u'长度不对'
	if min :
		ret += u'，不得少于%s字符' % (min)
	if max :
		ret += u'，不得多于%s字符' % (max)
	ret += u'。'
	return ret

USERNAME = u'用户'
PASSWORD = u'密码'
NEWPASSWORD = u'新密码'
EMAIL = u'邮箱'
ERROR_NOT_MATCH = u'两次输入的数据不一样。'
ERROR_NOT_EMAIL = u'在下判断这不是邮箱地址。'

class UserForm(Form) :
	username = StringField('username', 
				validators = [DataRequired(message = ERROR_EMPTY(USERNAME)), 
					Length(max = 16, message = ERROR_LENGTH(USERNAME, max = 16))])
	password = PasswordField('password', 
				validators = [DataRequired(message = ERROR_EMPTY(PASSWORD)), 
					Length(max = 16, message = ERROR_LENGTH(PASSWORD, max = 16))])
	submit = SubmitField(u'submit')

class LoginForm(UserForm):
	remember_me = BooleanField(u'remember_me', default = False)


class RegisterForm(UserForm) :
	password = PasswordField('password', 
				validators = [DataRequired(message = ERROR_EMPTY(PASSWORD)), 
					EqualTo('confirm', message = ERROR_NOT_MATCH), 
					Length(max = 16, message = ERROR_LENGTH(PASSWORD, max = 16))])
	confirm  = PasswordField('repeatPassword')
	email = StringField('emailaddress', 
				validators = [DataRequired(message = ERROR_EMPTY(EMAIL)), 
					Length(max = 64, message = ERROR_LENGTH(EMAIL, max = 64)), 
					Email(message = ERROR_NOT_EMAIL)])

class EditForm(UserForm) :
	newPassword = PasswordField('password', 
				validators = [
					EqualTo('confirm', message = ERROR_NOT_MATCH), 
					Length(max = 16, message = ERROR_LENGTH(NEWPASSWORD, max = 16))])
	confirm  = PasswordField('repeatPassword')
	email = StringField('emailaddress', 
				validators = [DataRequired(message = ERROR_EMPTY(EMAIL)), 
					Length(max = 64, message = ERROR_LENGTH(EMAIL, max = 64)), 
					Email(message = ERROR_NOT_EMAIL)])

FILENAME = u'文件名称'
FILE = u'试题'
SUBJECT = u'科目'
class UploadForm(Form) :
	file = TextAreaField('file', 
				validators = [DataRequired(message = ERROR_EMPTY(FILE))])
	answer = TextAreaField('answer')
	filename = StringField('filename', 
				validators = [DataRequired(message = ERROR_EMPTY(FILENAME)), 
					Length(min = 2, max = 256, 
						message = ERROR_LENGTH(FILENAME, min = 2, max = 256))])
	subject = SelectField('subject', coerce = int, 
		validators = [DataRequired(message = ERROR_EMPTY(SUBJECT))])
	submit = SubmitField(u'submit')

SUGGEST = u'建议'
class SuggestionForm(Form) :
	suggestion = TextAreaField('suggestion', 
		validators = [DataRequired(message = ERROR_EMPTY(SUGGEST)), 
			Length(max = 256, message = ERROR_LENGTH(SUGGEST, max = 256))])
	submit = SubmitField(u'submit')

TIMEDELTA = u'时间范围'
class SearchProblemForm(Form) :
	subject = SelectField('subject', coerce = int, 
				validators = [DataRequired(message = ERROR_EMPTY(SUBJECT))])
	filename = StringField('filename')
	timeDelta = SelectField('timedelta', coerce = int)
	submit = SubmitField(u'submit')
							
# SelectField->coerce is the return type, which is the first part of choices

class ChoiceForm(Form) :
	option = BooleanField('option', default = False)
	description = ""

class ProblemForm(Form) :
	pid = int
	index = int
	description = u''
	choices = []
	# The return value is a list
	check = 0
	message = ''
	realAnswer = ''
	singleSelect = False
	# 0 -> unSelect  1 -> Wrong  2 -> Right

class BrushForm(Form) :
	pro = []
	submit = SubmitField(u'submit')
	hideCorrectProblem = BooleanField('hideCorrectProblem', default = False)
	title = u''
	