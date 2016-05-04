# -*- coding: utf-8 -*-

from flask import Flask, request, session, \
					g, redirect, url_for, \
					abort, render_template, flash,  \
					Blueprint
from flask.ext.login import current_user, login_required
from apps import app, db, models
from apps.forms import SearchProblemForm, ProblemForm, BrushForm
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
	results = models.Document.query.\
					filter(models.Document.timeStamp >= startTime)\
					.whoosh_search(name, limit = 50).all()
	result = []
	for x in results :
		result.append((x.id, x.title))
	return render_template('viewproblems/showresult.html', result = result)

def myValidate(arrayForm) :
	for x in arrayForm :
		if not x.validate_on_submit() :
			return False
	return True

@viewproblems.route('/show/<int:did>', methods=['GET', 'POST'])
def show(did) :
	allCorret = False
	if 'allProblem' not in dir() :
		doc = models.Document.query.filter(models.Document.id == did).first()
		allProblem = BrushForm()
		count = 0
		for x in doc.problems :
			count += 1
			# description = str(count) + u'、' + x.content.title()
			# Use ol/li to index the problems
			description = x.content.title()
			choices = x.choice.split(u'##')
			index = 0
			choices = []
			for y in choices :
				y = y.strip()
				if len(y) > 0 :
					choicesDescription += \
						unicode(app.config['CHOICE_INDEX'][index]) + \
						u'、' + unicode(y)
					
					choices.append((app.config['CHOICE_INDEX'][index],
									choicesDescription))
					countChoice += 1
			
			pro = ProblemForm()
			pro.pid = x.id
			pro.index = count
			pro.description = description
			pro.choice.choices = choices
			pro.choice.default = []
			pro.check = 0
			allProblem.pro.append(pro)
	elif request.method == 'POST' and myValidate(allProblem.pro) :
		allCorret = True
		for x in allProblem.pro :
			if len(x.choice.data) < 1 :
				allCorret = False
				x.check = 0
				continue
			realPro = models.Problem.query.filter(models.Problem.id == x.pid)
			realPro = realPro.first()
			answer = unicode(realPro.answer)
			customAnswer = unicode(''.join(x.choice.data))
			if customAnswer == answer :
				x.check = 2
				x.message = app.config['MESSAGE_FOR_RIGHT']
			else :
				x.check = 1
				allCorret = False
				x.message = app.config['MESSAGE_FOR_WRONG'] % (realPro.answer)
	
	if allCorret == False :
		return render_template('viewproblems/showproblems.html', 
								papers = allProblem)
	else :
		return render_template('viewproblems/congratulation.html')
	
				