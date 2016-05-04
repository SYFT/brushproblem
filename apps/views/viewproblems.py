# -*- coding: utf-8 -*-

from flask import Flask, request, session, \
					g, redirect, url_for, \
					abort, render_template, flash,  \
					Blueprint
from flask.ext.login import current_user, login_required
from apps import app, db, models
from apps.forms import SearchProblemForm, ProblemForm, BrushForm, ChoiceForm
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
		allProblem.pro = []
		count = 0
		for x in doc.problems :
			count += 1
			# description = str(count) + u'、' + x.content.title()
			# Use ol/li to index the problems
			description = x.content.title()
			choices = x.choice.split(u'##')
			print 'x.choice:', x.choice
			index = 0
			countChoice = 0
			pro = ProblemForm()
			pro.choices = []
			for y in choices :
				y = y.strip()
				if len(y) > 0 :
					option = unicode(app.config['CHOICE_INDEX'][index])
					choicesDescription = \
						option + \
						u'、' + unicode(y)
					
					thisChoice = ChoiceForm()
					thisChoice.option.default = False
					thisChoice.option.name = option
					thisChoice.option.id = option
					thisChoice.description = unicode(choicesDescription)
					pro.choices.append(thisChoice)
					countChoice += 1
			pro.pid = x.id
			pro.index = count
			pro.description = description
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
	
				