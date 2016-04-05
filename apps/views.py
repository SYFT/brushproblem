from apps import app
from flask import Flask, request, session, g, redirect, url_for, \
	 abort, render_template, flash
from .forms import LoginForm

@app.route('/')
@app.route('/index/')
def index():
	#user = {'username' : 'admin'}
	return render_template('index.html', userstatus = False)
	#return "Hello World"

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash('OpenID: ' + form.openid.data + '\n')
		flash('remember_me : ' + str(form.remember_me.data) + '\n')
		return redirect('/index')
	return render_template('login.html', 
							title = 'Sign In', 
							form = form,
							providers = app.config['OPENID_PROVIDERS'])

@app.route('/details')
def details():
	user = {'username' : 'yzx'}
	posts = [
		{'author' : user,
		'body' : 'a'},
		{'author' : user,
		'body' : 'b'}
	]
	return render_template('details.html', titile = 'Home', user = user, posts = posts)
