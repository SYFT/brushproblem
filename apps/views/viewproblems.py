# -*- coding: utf-8 -*-

from flask import Flask, request, session, \
					g, redirect, url_for, \
					abort, render_template, flash,  \
					Blueprint
from flask.ext.login import current_user, login_required
from apps import app, db, models
from apps.forms import SearchProblemForm
import datetime
import flask.ext.whooshalchemy

viewproblems = Blueprint('viewproblems', __name__, 
					static_folder = 'static',
					template_folder = 'templates')

@viewproblems.route('/search', methods=['GET', 'POST'])
def search() :
	if 'form' not in dir() :
		form = SearchProblemForm()
		categories = models.Subject.query.order_by('name')
		
		nameOfCategories = []
		for x in categories :
			nameOfCategories.append((x.id, x.name))
		form.subject.choices = nameOfCategories
		
		typeOfTimeDelta = []
		for x, y in app.config['TIMEDELTA_CHOICE'] :
			typeOfTimeDelta.append((x, y))
		form.timeDelta.choices = typeOfTimeDelta
		form.timeDelta.data = app.config['DEFAULT_TIME_DELTA']
	
	if request.method == 'POST' and form.validate_on_submit() :
		name = form.filename.data
		category = form.subject.data
		timeDelta = form.timeDelta.data
		print 'Good'
		return redirect(url_for('viewproblems.showResult', category = category, 
							name = name, timeDelta = timeDelta))
		
	return render_template('viewproblems/search.html', 
							title = u'Select your want!',
							form = form)

@viewproblems.route('/show/<int:category>&<string:name>&<int:timeDelta>', methods = ['GET'])
def showResult(category, name, timeDelta) :
	timeDelta = app.config['TIMEDELTA'][timeDelta]
	startTime = datetime.datetime.utcnow() - timeDelta
	results = models.Document.query.whoosh_search(name, limit = 50).all()
	result = []
	for x in results :
		result.append((x.id, x.title))
	return render_template('viewproblems/showresult.html', result = result)

@viewproblems.route('/show/<int:pid>')
def show(pid) :
	pass
							