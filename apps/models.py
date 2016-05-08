# -*- coding: utf-8 -*-

import datetime, flask.ext.whooshalchemy
from apps import app, db
from flask.ext.MyImport import jieba

class User(db.Model) :
	__searchable__ = ['username']

	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(16, convert_unicode = True), index = True, unique = True)
	password = db.Column(db.String(32))
	email = db.Column(db.String(64), index = True)
	isAdmin = db.Column(db.Boolean)
	contributions = db.relationship('Document', backref = 'author', lazy = 'dynamic')
	
	def __init__(self, username, password, email, isAdmin = False) :
		self.username = username
		self.password = password
		self.email = email
		self.isAdmin = isAdmin
	
	def __repr__(self) :
		return self.username
	
	def is_authenticated(self) :
		return True
		
	def is_active(self) :
		return True
	
	def is_anonymous(self) :
		return True
	
	def get_id(self) :
		return unicode(self.id)
	
		
class Document(db.Model) :
	__searchable__ = ['keywordsForTitle']
	
	id = db.Column(db.Integer, primary_key = True)
	userId = db.Column(db.Integer, db.ForeignKey('user.id'))
	subjectId = db.Column(db.Integer, db.ForeignKey('subject.id'))
	title = db.Column(db.Unicode(256), index = True)
	keywordsForTitle = db.Column(db.Unicode(512), index = True)
	timeStamp = db.Column(db.DateTime, index = True)
	problems = db.relationship('Problem', backref = 'source', lazy = 'dynamic')
	
	def __init__(self, title, author, subjectId, timeStamp = datetime.datetime.utcnow()) :
		self.title = unicode(title)
		self.author = author
		self.subjectId = subjectId
		self.timeStamp = timeStamp
		result = jieba.cut_for_search(title)
		result = list(result)
		l = ' '.join(result)
		self.keywordsForTitle = unicode(l)
		print 'okay'
	
	def __repr__(self) :
		return self.title

class Problem(db.Model) :
	id = db.Column(db.Integer, primary_key = True)
	documentId = db.Column(db.Integer, db.ForeignKey('document.id'))
	content = db.Column(db.Unicode(512))
	choice = db.Column(db.Unicode(512))
	answer = db.Column(db.Unicode(128))
#	content is in this format :
#	problem description
#	choice is in this format :
#	##choose description##choose description## .... 
#	caution : () are needed.
#	answer is in this format : ABCD/A/BC
#	multianswers must be splited by _ if necessary.
	
	def __init__(self, source, content, choice, answer) :
		self.source = source
		self.content = unicode(content)
		self.choice = unicode(choice)
		self.answer = unicode(answer)
	
	def __repr__(self) :
		return '<Problem %d : \n %r \n %r \n>' % (self.id, self.content, self.answer)
		

class Subject(db.Model) :
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.Unicode(32), index = True)
	ducuments = db.relationship('Document', backref = 'category', lazy = 'dynamic')

	def __init__(self, name) :
		self.name = unicode(name)

	def __repr__(self) :
		return self.name

		

from flask.ext.admin import Admin, BaseView, expose
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.login import current_user
from flask import session

class MyView(BaseView) :
	def is_accessible(self) :
		try :
			# user = current_user
			# print '%s isAdmin:' % (user.username), user.isAdmin
			# print (user.is_authenticated() and user.isAdmin)
			if (user.is_authenticated() and user.isAdmin and session['_fresh'] == True) :
				# print 'here return True'
				return True
			# print 'here return False'
		except Exception as e :
			pass
		return False
	
	@expose('/')
	def index(self) :
		return self.render('admin/adminindex.html')

class MyModelView(ModelView) :
	def is_accessible(self) :
		user = current_user
		try :
			print 'fresh:', session['_fresh']
			if (user.is_authenticated() and user.isAdmin and session['_fresh'] == True):
				return True
		except Exception as e :
			pass
		return False


