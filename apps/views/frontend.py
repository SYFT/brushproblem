from flask import Flask, Blueprint, render_template, \
					g, url_for, session, request
from flask.ext.login import login_required, \
					current_user, login_required
from apps.forms import SuggestionForm
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
	
@frontend.route('/FAQ', methods = ['POST', 'GET'])
def faq() :
	form = SuggestionForm()
	print '#######\n\n\n\n  here'
	print '###', form.suggestion
	return render_template('frontend/faq.html', form = form)

@frontend.route('/tha')
def suggest() :
	flash('Having receive!!!')
	return render_template('frontend/index.html')
