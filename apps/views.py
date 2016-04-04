from apps import app
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

@app.route('/')
@app.route('/index/<status>')
def index(status = False):
	#user = {'username' : 'admin'}
	return render_template('index.html', userstatus = status)
	#return "Hello World"

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or \
           request.form['password'] != 'secret':
            flash(u'Invalid username or assword')
            error = 'Invalid credentials'
        else:
            flash('You were successfully logged in')
            flash('Welcome back %s' % request.form['username'])
            return redirect(url_for('index', status = True))
    return render_template('login.html', error=error)

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
