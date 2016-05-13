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
	for pro in arrayForm :
		if not pro.validate_on_submit() :
			return False
		for choice in pro.choices :
			if not choice.validate_on_submit() :
				return False
	return True

@viewproblems.route('/show/<int:did>', methods=['GET', 'POST'])
def show(did = None, tempfile = None) :
	print 'request.form:', request.form
	allCorret = False
	
	# 定义表格
	if 'allProblem' not in dir() :
		if not did and tempfile :
			doc = tempfile
		else :
			doc = models.Document.query.filter(models.Document.id == did).first()
		allProblem = BrushForm()
		allProblem.pro = []
		count = 0
		allProblem.title = doc.title
		for x in doc.problems :
			count += 1
			# description = str(count) + u'、' + x.content.title()
			# Use ol/li to index the problems
			description = x.content.title()
			choices = x.choice.split(u'##')
			# print 'x.choice:', x.choice
			# print 'x.answer:', x.answer
			countChoice = 0
			pro = ProblemForm()
			pro.choices = []
			for y in choices :
				y = y.strip()
				if len(y) > 0 :
					option = chr(countChoice + ord('A'))
					choicesDescription = \
						option + \
						u'、' + unicode(y)
					
					thisChoice = ChoiceForm()
					thisChoice.option.default = False
					thisChoice.option.name = unicode(count)
					thisChoice.option.id = unicode(count)
					thisChoice.option.userValue = option
					thisChoice.description = unicode(choicesDescription)
					pro.choices.append(thisChoice)
					countChoice += 1
			pro.pid = x.id
			pro.index = count
			pro.description = description
			pro.check = 0
			allProblem.pro.append(pro)
	
	# 将传过来的表单填写入对应的表格位置
	if request.method == 'POST' :
		for pro in allProblem.pro :
			userChoices_list = request.form.getlist(str(pro.index))
			for c in userChoices_list :
				index = ord(c) - ord('A')
				# pro.choices[index].option.checked = True
				pro.choices[index].option.data = True
		# print request.Form['1']
	
	# 检查答案，给予反馈
	if allProblem.validate_on_submit() and myValidate(allProblem.pro) :
		allCorret = True
		for pro in allProblem.pro :
			userAnswer = unicode('')
			choiceIndex = 0
			for choice in pro.choices :
				# print choice.option.data
				if choice.option.data == True :
					userAnswer += unicode(chr(choiceIndex + ord('A')))
				choiceIndex += 1
			userAnswer = userAnswer.strip()
			# print pro.index, ':', userAnswer
			
			if len(userAnswer) < 1 :
				pro.check = 0
				allCorret = False
				continue
			
			realPro = models.Problem.query.filter(models.Problem.id == pro.pid)
			realPro = realPro.first()
			answer = unicode(realPro.answer)
			
			if userAnswer == answer :
				pro.check = 2
				pro.message = app.config['MESSAGE_FOR_RIGHT']
			else :
				pro.check = 1
				allCorret = False
				pro.message = app.config['MESSAGE_FOR_WRONG'] % (realPro.answer)
	
	print 'how allproblems:', 'allProblem' in dir()
	if allCorret == False :
		return render_template('viewproblems/showproblems.html', 
								index = did, papers = allProblem)
	else :
		return render_template('viewproblems/congratulation.html')
	
				