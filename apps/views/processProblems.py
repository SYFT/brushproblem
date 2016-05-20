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
	print 'search begin'
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
	if request.method == 'GET' :
		form.timeDelta.data = app.config['DEFAULT_TIME_DELTA']
	
	print 'search fine'
	# print 'data:', form.timeDelta.data
	
	if request.method == 'POST' and form.validate_on_submit() :
		name = form.filename.data
		category = form.subject.data
		timeDelta = form.timeDelta.data
		# print 'Good'
		return redirect(url_for('processProblems.showResult', category = category, 
							name = name, timeDelta = timeDelta))
	
	docs = models.Document.query.all()
	numberOfDocuments = len(docs)
	listOfRecentDocument = models.Document.query.\
								limit(numberOfDocuments).from_self().\
								order_by(models.Document.timeStamp)
	listOfRecentDocument = list(listOfRecentDocument)
	listOfRecentDocument.reverse()
	listOfRecentDocument = listOfRecentDocument[0:7]
	
	return render_template('processProblems/search.html', 
							title = u'Select your want!',
							form = form,
							listOfRecentDocument = listOfRecentDocument)

@processProblems.route('/show/<int:category>&<string:name>&<int:timeDelta>', methods = ['GET'])
def showResult(category, name, timeDelta) :
	print timeDelta
	timeDelta = app.config['TIMEDELTA'][timeDelta]
	startTime = datetime.datetime.utcnow() - timeDelta
	print datetime.datetime.utcnow()
	print timeDelta
	print startTime
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
		try :
			if documentId < 6666666 :
				doc = models.Document.query.filter(models.Document.id == documentId).first()
				print 'doc,', doc
				if doc is None :
					raise Exception(app.config['HOWDOYOUFINDTHISPAGE'])
			else :
				documentId = session['tempfile']
				doc = models.Document.query.filter(models.Document.id == documentId).first()
				if doc is None :
					raise Exception(app.config['NOSUCHFILE'])
				pros = []
				for pro in doc.problems :
					pros.append((pro.content, pro.choice, pro.answer))
				tempfile = models.Tempfile(doc.title, pros)
				g.doc = tempfile
		except Exception as e :
			print e
			flash(e.message)
			print 'hello'
			return redirect(url_for('processProblems.search'))
		allProblem = getAllProblem(doc)
	
	# 将传过来的表单填写入对应的表格位置
	userLogin = ('user' in session and session['user'] == current_user.id)
	userLastSubmitDict = {}
	if userLogin :
		u = models.User.query.filter(models.User.id == current_user.id).first()
		if u.lastVisit == documentId :
			# print u.lastSubmit
			tmpAnswer = u.lastSubmit.split('##')
			print 'dddd'
			print tmpAnswer
			temp = []
			for x in tmpAnswer :
				if len(x) > 0 :
					temp.append(x)
			tmpAnswer = temp
			length = len(tmpAnswer) / 2
			for i in range(0, length) :
				print int(tmpAnswer[2 * i]), unicode(tmpAnswer[2 * i + 1])
				userLastSubmitDict[int(tmpAnswer[2 * i])] = unicode(tmpAnswer[2 * i + 1])
	
	if request.method == 'POST' :
		print 'POST'
		recordUserId = documentId
		recordUserAnswer = ''
		for pro in allProblem.pro :
			# print pro.index
			userChoices_list = request.form.getlist(str(pro.index))
			# print pro.index, userChoices_list
			# if len(userChoices_list) < 1 and userLogin :
				# if userLastSubmitDict.has_key(pro.index) :
					# userChoices_list = userLastSubmitDict[pro.index]
			
			tmpAnswer = ''
			for c in userChoices_list :
				index = ord(c) - ord('A')
				# pro.choices[index].option.checked = True
				pro.choices[index].option.data = True
				tmpAnswer += c
			
			if len(tmpAnswer) > 0 :
				# print tmpAnswer
				recordUserAnswer += unicode(pro.index) + "##"
				recordUserAnswer += tmpAnswer + "##"
		
		try :
			# print 'userLogin', userLogin
			# print 'recordUserId', recordUserId
			# print 'recordUserAnswer', recordUserAnswer
			if userLogin and len(recordUserAnswer) > 0 :
				u = models.User.query.filter(models.User.id == current_user.id).first()
				u.lastVisit = recordUserId
				u.lastSubmit = recordUserAnswer
				db.session.commit()
				# print 'record:', recordUserAnswer
		except Exception as e :
			print 'error', e
			pass
	elif userLogin :
		for pro in allProblem.pro :
			# print pro.index
			userChoices_list = ''
			if userLastSubmitDict.has_key(pro.index) :
				userChoices_list = userLastSubmitDict[pro.index]
			for c in userChoices_list :
				index = ord(c) - ord('A')
				pro.choices[index].option.data = True
	
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
			# print "here"
			try :
				
				title = form.filename.data
				title = title.title()
				# print title
				content = form.file.data
				# print 'content:', content
				# print ord(content[24])
				answer = None
				if form.answer.data :
					answer = form.answer.data
				category = form.subject.data
				
				print 'begin change'
				format_content = change(content, answer)
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