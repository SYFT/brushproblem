from flask import Flask, request, session, \
					g, redirect, url_for, \
					abort, render_template, flash,  \
					Blueprint
from flask.ext.login import current_user, login_required
from apps import db, models

viewproblems = Blueprint('viewproblems', __name__, 
					static_folder = 'static',
					template_folder = 'templates')

@viewproblems.route('/search', methods=['GET', 'POST'])
def search() :
	
	return render_template('viewproblems/search.html', title = u'Select your want!')
