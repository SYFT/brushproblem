# -*- coding: utf-8 -*-

from flask import Flask, request, session, \
					g, redirect, url_for, \
					abort, render_template, flash,  \
					Blueprint
from flask.ext.login import current_user, login_required
from apps import app, db, models
from apps.forms import SearchProblemForm, ProblemForm, BrushForm, ChoiceForm,\
						UploadForm
import datetime, re
import flask.ext.whooshalchemy
from apps.models import MyOperateError
from processMethods import *

processProblems = Blueprint('processProblems', __name__, 
					static_folder = 'static',
					template_folder = 'templates')

@processProblems.route('/search', methods=['GET', 'POST'])
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
		# print 'Good'
		return redirect(url_for('processProblems.showResult', category = category, 
							name = name, timeDelta = timeDelta))
		
	return render_template('processProblems/search.html', 
							title = u'Select your want!',
							form = form)

@processProblems.route('/show/<int:category>&<string:name>&<int:timeDelta>', methods = ['GET'])
def showResult(category, name, timeDelta) :
	timeDelta = app.config['TIMEDELTA'][timeDelta]
	startTime = datetime.datetime.utcnow() - timeDelta
	results = models.Document.query.\
					filter(models.Document.timeStamp >= startTime)\
					.whoosh_search(name, limit = 50).all()
	result = []
	for x in results :
		result.append((x.id, x.title))
	return render_template('processProblems/showresult.html', result = result)

@processProblems.route('/show/<did>', methods = ['GET', 'POST'])
def show(did) :
	print 'yyyyyyyyyyyyyyyyyy'
	
	print 'request.form:', request.form
	allCorret = False
	
	# 定义表格
	if 'allProblem' not in dir() :
		# print 'not define'
		# print did
		# print session
		documentId = int(did)
		if documentId < 6666666 :
			doc = models.Document.query.filter(models.Document.id == documentId).first()
		else :
			documentId = session['tempfile']
			doc = models.Document.query.filter(models.Document.id == documentId).first()
			pros = []
			for pro in doc.problems :
				pros.append((pro.content, pro.choice, pro.answer))
			tempfile = models.Tempfile(doc.title, pros)
			g.doc = tempfile
		allProblem = getAllProblem(doc)
	
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
			
			answer = unicode(pro.realAnswer)
			
			if userAnswer == answer :
				pro.check = 2
				pro.message = app.config['MESSAGE_FOR_RIGHT']
			else :
				pro.check = 1
				allCorret = False
				pro.message = app.config['MESSAGE_FOR_WRONG'] % (pro.realAnswer)
	
	print 'how allproblems:', 'allProblem' in dir()
	if allCorret == False :
		return render_template('processProblems/showproblems.html', 
								index = did, papers = allProblem)
	else :
		return render_template('processProblems/congratulation.html')

def addSessionTempFile(x) :
	if 'tempfile' in session :
		try :
			docId = session['tempfile']
			if docId != x :
				doc = models.Document.query.filter(models.Document.id == docId).first()
				db.session.delete(doc)
				db.session.commit()
		except Exception as e :
			print 'No such file'
		
		session.pop('tempfile', None)
	session['tempfile'] = x
	# print session
		
@processProblems.route('/upload', methods = ['GET', 'POST'])
@login_required
def upload() :
	if 'form' not in dir() :
		form = UploadForm()
		categories = models.Subject.query.order_by('name')
		nameOfCategories = []
		for x in categories :
			nameOfCategories.append((x.id, x.name))
		form.subject.choices = nameOfCategories
	
	
	# if 'form' in dir() :
		# print 'hhhhhhh'
		# print form.validate_on_submit()
		# print form.subject.data
		# print form.subject.choices
		# print form.filename.data
		# print form.file.data
		# print request.method
		# print form.errors
	
	if request.method == 'POST' :
		if form.validate_on_submit() :
			print "here"
			try :
				
				title = form.filename.data
				print title
				content = form.file.data
				# print ord(content[24])
				category = form.subject.data
				
				print 'begin change'
				format_content = change(content)
				print 'end change'
	#			format_content should be a pair list
	#			the first element should be problem's description
	#			the second element should be problem's answer
				
				# print format_content
				# for x, y, z in format_content :
					# print x.encode('gb2312'), y.encode('gb2312'), z.encode('gb2312')
				
				if len(format_content) < 2 :
					raise MyOperateError('The number of problems is too small. \
											Only %d problems found' % (len(format_content)))
				
				
				# print 'fine'
				
				doc = models.Document(title = title, author = current_user, subjectId = category)
				db.session.add(doc)
				db.session.commit()
				for content, choices, answer in format_content :
					pro = models.Problem(source = doc, content = content, choice = choices, answer = answer)
					db.session.add(pro)
				db.session.commit()
				
				flash(app.config['SUCCESS_PROCESS'])
				if current_user.isAdmin == True :
					return redirect(url_for('processProblems.show', 
									did = unicode(doc.id)))
				else :
					# print session
					addSessionTempFile(doc.id)
					# print session
					# print title
					# print 'session:', session['tempfile'][0]
					return redirect(url_for('processProblems.show', 
									did = unicode(6666666)))
			except MyOperateError as e:
				print '\n\n\n xxx :', e.description
				print '\r\n\r\n\r\n\r\n\r\n\r\n\r\n\n'
				flash(app.config['FAIL_PROCESS'])
			except Exception as e:
				print '\n\n\n yyy :', e
				print '\r\n\r\n\r\n\r\n\r\n\r\n\r\n\n'
				flash(app.config['FAIL_PROCESS'])
		else :
			if current_user.isAdmin :
				flash(app.config['FAIL_UPLOAD'])
			else :
				flash(app.config['FAIL_PROCESS'])
	return render_template('processProblems/upload.html', form = form)