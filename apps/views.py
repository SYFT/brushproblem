from apps import app, db, lm, openID
from flask import Flask, request, session, g, redirect, url_for, \
					abort, render_template, flash
from .forms import LoginForm
from flask.ext.login import login_user, logout_user, \
							current_user, login_required
from .models import *

@app.route('/')
@app.route('/index/')
def index():
	return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
@openID.loginhandler
def login():
	if g.user is not None and g.user.is_authenticated == True:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		flash('username: ' + form.username.data + '\n')
		flash('remember_me : ' + str(form.remember_me.data) + '\n')
		session['remember_me'] = form.remember_me.data
		return openID.try_login(form.openid.data, ask_for = ['email'])
	return render_template('login.html', title = 'Sign In', form = form, providers = app.config['OPENID_PROVIDERS'])

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))

@lm.user_loader
def load_user(id) :
	return User.query.get(int(id))
	
@app.before_request
def before_request():
	g.user = current_user

@openID.after_login
def after_login(resp):
	flash('here')
	if resp.email is None or resp.email == "":
		flash('Invalid login. Please try again.')
		return redirect(url_for('login'))
	user = User.query.filter_by(email = resp.email).first()
	if user is None:
		#username = resp.username
		if username is None or username == "":
			username = resp.email.split('@')[0]
		user = User(username = username, password = '123456', email = resp.email)
		db.session.add(user)
		db.session.commit()
	remember_me = False
	if 'remember_me' in session:
		remember_me = session['remember_me']
		session.pop('remember_me', None)
	login_user(user, remember = remember_me)
	return redirect(url_for('index'))
		
@app.route('/details')
@app.login_required
def details():
	user = {'username' : 'yzx'}
	posts = [
		{'author' : user,
		'body' : 'a'},
		{'author' : user,
		'body' : 'b'}
	]
	return render_template('details.html', titile = 'Home', user = user, posts = posts)
