# -*- coding: utf-8 -*-

import datetime, flask.ext.whooshalchemy
from apps import app, db

class User(db.Model) :
	__searchable__ = ['username']

	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(16), index = True, unique = True)
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
	__searchable__ = ['title']
	
	id = db.Column(db.Integer, primary_key = True)
	userId = db.Column(db.Integer, db.ForeignKey('user.id'))
	subjectId = db.Column(db.Integer, db.ForeignKey('subject.id'))
	title = db.Column(db.String(256), index = True)
	timeStamp = db.Column(db.DateTime, index = True)
	problems = db.relationship('Problem', backref = 'source', lazy = 'dynamic')
	
	def __init__(self, title, author, subjectId, timeStamp = datetime.datetime.utcnow()) :
		self.title = title
		self.author = author
		self.subjectId = subjectId
		self.timeStamp = timeStamp
	
	def __repr__(self) :
		return '<Title % r>' % (self.title)

class Problem(db.Model) :
	id = db.Column(db.Integer, primary_key = True)
	documentId = db.Column(db.Integer, db.ForeignKey('document.id'))
	content = db.Column(db.String(512))
	choice = db.Column(db.String(512))
	answer = db.Column(db.String(128))
#	content is in this format :
#	problem description
#	answer is in this format :
#	(choose description) (choose description) .... 
#	caution : () are needed.
#	answer is in this format : A_B_C_D/A/B_C
#	multianswers must be splited by _ if necessary.
	
	def __init__(self, source, content, choice, answer) :
		self.source = source
		self.content = content
		self.choice = choice
		self.answer = answer
	
	def __repr__(self) :
		return '<Problem %d : \n %r \n %r \n>' % (self.id, self.content, self.answer)
		

class Subject(db.Model) :
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(32), index = True)
	ducuments = db.relationship('Document', backref = 'category', lazy = 'dynamic')

	def __init__(self, name) :
		self.name = name

	def __repr__(self) :
		return '<Subject %r>' % (self.name)

		
# 每个希望可以被检索的表都要被whoosh_index
flask.ext.whooshalchemy.whoosh_index(app, User)
flask.ext.whooshalchemy.whoosh_index(app, Document)
