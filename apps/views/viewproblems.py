from flask import Flask, request, session, \
					g, redirect, url_for, \
					abort, render_template, flash,  \
					Blueprint
from flask.ext.login import current_user, login_required
from apps import db, models
from apps.forms import SearchProblemForm
import datetime

viewproblems = Blueprint('viewproblems', __name__, 
					static_folder = 'static',
					template_folder = 'templates')

@viewproblems.route('/search', methods=['GET', 'POST'])
def search() :
	form = SearchProblemForm()
	categories = models.Subject.query.order_by('name')
	nameOfCategories = []
	for x in categories :
		nameOfCategories.append((x.id, x.name))
	form.subject.choices = nameOfCategories
	if request.method == 'POST' and form.validate_on_submit() :
		timeDelta = form.timeDelta.data
		name = form.filename.data
		category = form.subject.data
		
		return redirect(url_for('showResult', category = category, 
							name = name, timeDelta = timeDelta))
		
	return render_template('viewproblems/search.html', 
							title = u'Select your want!',
							form = form)

@viewproblems.route('/show', methods = ['GET'])
def showResult(category, name, timeDelta) :
	startTime = datetime.datetime.utcnow() - timeDelta
	results = models.Document.query.filter_by(
				Dcoument.timeStamp >= startTime, 
				subjectID == category).whoosh_search(name, limits = 50).all()
	result = []
	for x in results :
		result.append((x.id, x.title))
	return render_template(url_for('viewproblems/showresult.html', 
							result = result))
							