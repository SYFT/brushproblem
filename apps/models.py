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
		return '<User % r>' % (self.username)
	
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
		print 'xxxx'
		print ' '.join(result)
		l = ' '.join(result)
		self.keywordsForTitle = unicode(l)
	
	def __repr__(self) :
		return '<Title % r>' % (self.title)

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
#	answer is in this format : A_B_C_D/A/B_C
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
		return '<Subject %r>' % (self.name)

		
# 每个希望可以被检索的表都要被whoosh_index
flask.ext.whooshalchemy.whoosh_index(app, User)
flask.ext.whooshalchemy.whoosh_index(app, Document)
