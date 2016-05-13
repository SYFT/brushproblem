from flask import Flask, Blueprint, render_template, \
					g, url_for, session, request, flash, \
					redirect
from flask.ext.login import login_required, \
					current_user, login_required,\
					fresh_login_required
from apps.forms import SuggestionForm, EditForm
frontend = Blueprint('frontend', __name__, 
					static_folder = 'static',
					template_folder = 'templates')
from apps import models, app, db
					
@frontend.before_request
def before_request() :
	g.user = current_user
					
@frontend.route('/')
@frontend.route('/index/')
def index():
	# if '_fresh' in session :
		# print session['_fresh']
	# if 'user' in session : 
		# print session['user']
	return render_template('frontend/index.html')
	
@frontend.route('/details')
@login_required
def details(uid = None):
	if not uid :
		uid = current_user.id
	u = models.User.query.filter(models.User.id == uid).first()
	docs = []
	for x in u.contributions :
		docs.append(x)
	
	return render_template('frontend/details.html', 
							titile = 'Home', 
							username = u.username, 
							docs = docs)
	
@frontend.route('/FAQ', methods = ['POST', 'GET'])
def faq() :
	form = SuggestionForm()
	# print '#######\n\n\n\n  here'
	# print '###', form.suggestion.data
	return render_template('frontend/faq.html', form = form)

@frontend.route('/Thank', methods = ['POST', 'GET'])
def suggest() :
	flash('Having receive!!!')
	return render_template('frontend/index.html')

@frontend.route('/edit', methods = ['POST', 'GET'])
# @login_required
@fresh_login_required
def changeUserDetails() :
	user = current_user
	form = EditForm()
	u = models.User.query.filter(models.User.id == user.id).first()
	
	if not form.username.data :
		form.username.data = u.username
	if not form.email.data :
		form.email.data = u.email
	
	# print 'form.validate_on_submit:', form.validate_on_submit()
	if request.method == 'POST' and form.validate_on_submit() :
		# print 'xxxxxxx'
		if u.password == form.password.data :
			u.username = form.username.data
			print form.newPassword.data
			if len(form.newPassword.data) > 0 :
				u.password = form.newPassword.data
			u.email = form.email.data
			flash('Succefully change!!')
			db.session.commit()
			# print 'yyyyy'
			return redirect(url_for('frontend.changeUserDetails'))
		else :
			# print 'xxxxx'
			flash(app.config['PASSWROD_NOT_MATCH'])
	
	return render_template('frontend/changeUserDetails.html', form = form)
