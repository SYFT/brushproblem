from flask import Flask, Blueprint, render_template, \
					g, url_for, session, request, flash
from flask.ext.login import login_required, \
					current_user, login_required
from apps.forms import SuggestionForm, EditForm
frontend = Blueprint('frontend', __name__, 
					static_folder = 'static',
					template_folder = 'templates')
from apps import models
					
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
	user = current_user
	u = models.User.query.filter(models.User.id == user.id).first()
	docs = []
	for x in u.contributions :
		docs.append(x)
	
	return render_template('frontend/details.html', 
							titile = 'Home', 
							username = user.username, 
							docs = docs)
	
@frontend.route('/FAQ', methods = ['POST', 'GET'])
def faq() :
	form = SuggestionForm()
	print '#######\n\n\n\n  here'
	print '###', form.suggestion.data
	return render_template('frontend/faq.html', form = form)

@frontend.route('/Thank', methods = ['POST', 'GET'])
def suggest() :
	flash('Having receive!!!')
	return render_template('frontend/index.html')

@frontend.route('/edit', methods = ['POST', 'GET'])
def changeUserdetails() :
	user = current_user
	form = EditForm()
	
	if request.method == 'POST' and form.validate_on_submit() :
		u = models.User.query.filter(models.User.id == user.id).first()
		if u.password == form.oldpassword.data :
			u.username = form.username.data
			u.password = form.password
		else :
			flash(app.config['PASSWRODNOTMEET'])
