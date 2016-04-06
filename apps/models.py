from apps import db
import datetime

class User(db.Model) :
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(16), index = True, unique = True)
	password = db.Column(db.String(32))
	email = db.Column(db.String(64), index = True)
	isAdmin = db.Column(db.Boolean)
	contributions = db.relationship(u'Problem', backref = u'author', lazy = u'dynamic')
	
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
	
		
class Problem(db.Model) :
	id = db.Column(db.Integer, primary_key = True)
	userId = db.Column(db.Integer, db.ForeignKey(u'user.id'))
	title = db.Column(db.String(256), index = True)
	storage = db.Column(db.String(256), unique = True)
	timeStamp = db.Column(db.DateTime, index = True)
	
	def __init__(self, title, storage, author, timeStamp = datetime.datetime.utcnow()) :
		self.title = title
		self.storage = storage
		self.author = author
		self.timeStamp = timeStamp
	
	def __repr__(self) :
		return '<Title % r>' % (self.title)
	