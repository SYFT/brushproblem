from flask import Flask, Blueprint, render_template, \
					g, url_for, session
from flask.ext.login import login_required, \
					current_user, login_required

frontend = Blueprint('frontend', __name__, 
					static_folder = 'static',
					template_folder = 'templates')

@frontend.before_request
def before_request() :
	g.user = current_user
					
@frontend.route('/')
@frontend.route('/index/')
def index():
	if '_fresh' in session :
		print session['_fresh']
	if 'user' in session : 
		print session['user']
	return render_template('frontend/index.html')
	
@frontend.route('/details')
@login_required
def details():
	user = {'username' : 'yzx'}
	posts = [
		{'author' : user,
		'body' : 'a'},
		{'author' : user,
		'body' : 'b'}
	]
	return render_template('frontend/details.html', titile = 'Home', user = user, posts = posts)
	
@frontend.route('/FAQ')
def faq() :
	return render_template('frontend/faq.html')
