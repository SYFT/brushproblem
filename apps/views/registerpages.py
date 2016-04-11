from flask import Flask, request, session, \
					g, redirect, url_for, \
					abort, render_template, flash,  \
					Blueprint
from apps.forms import RegisterForm
from flask.ext.login import login_user, logout_user, \
							current_user, login_required
from apps import lm, db, models

registerpages = Blueprint('registerpages', __name__, 
					static_folder = 'static',
					template_folder = 'templates')

@registerpages.route('/register', methods = ['GET', 'POST'])
def register() :
	form = RegisterForm()
	if form.email.data : 
		flash(len(form.email.data))
	if form.validate_on_submit() :
		username = form.username.data
		password = form.password.data
		email = form.email.data
		
		queryByName = models.User.query.filter_by(username = username)
		if queryByName.first() is not None :
			flash(u'This username has been used')
		else :
			u = models.User(username = username, password = password, email = email)
			db.session.add(u)
			db.session.commit()
			flash(u'Successfully registed !!')
			return redirect(url_for('loginpages.login'))
	return render_template('registerpages/register.html', form = form)
