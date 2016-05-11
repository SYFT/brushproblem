from flask import Flask, request, session, \
					g, redirect, url_for, \
					abort, render_template, flash,  \
					Blueprint
from apps.forms import LoginForm
from flask.ext.login import login_user, logout_user, \
							current_user, login_required
from apps import lm, db, models

loginpages = Blueprint('loginpages', __name__, 
					static_folder = 'static',
					template_folder = 'templates')

def tryLogin(form) :
	username = form.username.data
	password = form.password.data
	remember_me = form.remember_me.data
	u = models.User.query.filter_by(username = username)
	u = list(u)
	if len(u) < 1 :
		flash('No such user')
		return redirect(url_for('loginpages.login'))
	
	u = u[0]
	if cmp(u.password, password) != 0 :
		flash('Invalid password')
		return redirect(url_for('loginpages.login'))
	if 'remember_me' in session :
		session['remember_me'] = None
	login_user(u, remember = remember_me)
	g.user = current_user
	session['user'] = g.user.id
	return redirect(request.args.get('next') or url_for('frontend.index'))

def checkAuthenticated(u) :
	if type(u.is_authenticated) == type(True) :
		return u.is_authenticated
	else :
		return u.is_authenticated()

	
@loginpages.before_request
def before_request():
	# print 'current_user:', current_user
	g.user = current_user
		
@loginpages.route('/login', methods=['GET', 'POST'])
def login() :
	# debug
	# if '_fresh' in session :
		# print session['_fresh']
	# print g.user
	# if 'user' in session : 
		# print session['user']
	# print 'user' in session
	
	# Have log in
	try :
		if 'user' in session and session['user'] == g.user.id :
			flash('you have been loggin in as %s.' % g.user.username)
			return redirect(url_for('frontend.index'))
	except Exception as e :
		pass
	
	form = LoginForm()
	if request.method == 'POST' and form.validate_on_submit():
		flash('username: ' + form.username.data + '\n')
		flash('remember_me : ' + str(form.remember_me.data) + '\n')
		return tryLogin(form)
	return render_template('loginpages/login.html', title = 'Sign In', form = form)	

@loginpages.route('/logout')
@login_required
def logout():
	session.pop('user', None)
	logout_user()
	return redirect(url_for('frontend.index'))


