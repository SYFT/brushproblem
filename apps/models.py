import datetime
from apps import db

class User(db.Model) :
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
	id = db.Column(db.Integer, primary_key = True)
	userId = db.Column(db.Integer, db.ForeignKey('user.id'))
	title = db.Column(db.String(256), index = True)
	timeStamp = db.Column(db.DateTime, index = True)
	problems = db.relationship('Problem', backref = 'source', lazy = 'dynamic')
	subject = db.Column(db.Integer, db.ForeignKey('category.id'), index = True)
	
	def __init__(self, title, author, timeStamp = datetime.datetime.utcnow()) :
		self.title = title
		self.author = author
		self.timeStamp = timeStamp
	
	def __repr__(self) :
		return '<Title % r>' % (self.title)

class Problem(db.Model) :
	id = db.Column(db.Integer, primary_key = True)
	documentId = db.Column(db.Integer, db.ForeignKey('document.id'))
	content = db.Column(db.String(512))

class Category(db.Model) :
	id = db.Column(db.Integer, primary_key = True)
	describtion = db.Column(db.String(32), index = True)
	ducuments = db.relationship('Problem', backref = 'source', lazy = 'dynamic')