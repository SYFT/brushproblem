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

def myValidate(arrayForm) :
	for pro in arrayForm :
		if not pro.validate_on_submit() :
			return False
		for choice in pro.choices :
			if not choice.validate_on_submit() :
				return False
	return True

def getAllProblem(doc) :
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
		try :
			pro.pid = x.id
			realPro = models.Problem.query.filter(models.Problem.id == pro.pid)
			realPro = realPro.first()
			pro.realAnswer = unicode(realPro.answer)
		except Exception as e :
			pro.realAnswer = x.answer
		pro.index = count
		pro.description = description
		pro.check = 0
		allProblem.pro.append(pro)
	return allProblem

@processProblems.route('/show/<did>', methods = ['GET', 'POST'])
def show(did) :
	print 'yyyyyyyyyyyyyyyyyy'
	
	# print 'request.form:', request.form
	allCorret = False
	
	# 定义表格
	if 'allProblem' not in dir() :
		# print 'not define'
		# print did
		documentId = int(did)
		if documentId < 6666666 :
			doc = models.Document.query.filter(models.Document.id == documentId).first()
		else :
			print g
			if 'doc' in g :
				doc = g.doc
			else :
				print session
				documentId = session['tempfile']
				session.pop('tempfile', None)
				doc = models.Document.query.filter(models.Document.id == documentId).first()
				g.doc = doc
				db.session.delete(doc)
				db.session.commit()
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

		
class MyOperateError(Exception) :
	description = ""

	def __init__(self, description = "Wrong in file!"):
		self.description = description
	
	def __repr__(self):
		return self.description
	
def change(x, documentType = 0) :
	# 0 -> 答案在括号中     1 -> 答案在全文最后
	if documentType == 0 :
		pat = re.compile(u'\r\n *[0-9]+[\.、,．､]|保险. ')
		problems = pat.split(x)
		# print problems
		ret = []
		for pro in problems :
			# print 'pro:', pro[0:24]
			if len(pro) < 3 :
				continue
			
			try :
			
				# Set the first letter in pro to be the answer
				# Get Answer from each problem
				getAnswer = False
				for reg in app.config['REGEX_ANSWER'] :
					pat = re.compile(reg)
					ansMatch = pat.search(pro)
					if ansMatch is None :
						# print 'hi'
						continue
					getAnswer = True
					
					while True :
						next = pat.search(pro, ansMatch.end())
						if next is None :
							break
						ansMatch = next
						# print ansMatch.start()
					
					answer = ansMatch.group()
					answer = answer.strip()
					
					pat = re.compile(u'[\(（\)）  ]')
					ans = pat.split(answer)
					answer = ''
					for i in range(0, len(ans)) :
						ans[i] = ans[i].strip()
						if len(ans[i]) > 0 :
							answer += ans[i]
					
					
					panDuanTi = False
					if answer in app.config['RIGHT_ANSWER'] or \
						answer in app.config['WRONG_ANSWER'] :
						if answer in app.config['RIGHT_ANSWER'] :
							answer = u'A'
						else :
							answer = u'B'
						panDuanTi = True
					
					pro = pro[:ansMatch.start()] + u'___' + pro[ansMatch.end():]
					
					break
				
				if getAnswer == False :
					# print '\r\n\r\n Wrong here:', pro
					# print '\r\n\r\n unicode here:', pro.decode('utf8')
					
					for reg in app.config['REGEX_ANSWER'] :
						pat = re.compile(reg)
						answer = pat.search(pro)
						# print answer
					raise MyOperateError(u'No Answer in brackets.')
				
				if not panDuanTi :
					# Get choices
					# Choices must be set in the tail of the problem
					
					getChoice = False
					for reg in app.config['REGEX_CHOICE'] :
						pat = re.compile(reg, re.S)
						allChoices = pat.search(pro)
						if allChoices is None :
							continue
						getChoice = True
					allChoices = allChoices.group()
					# print 'allchoices:', allChoices
					for reg in app.config['REGEX_CHOICE_INDEX'] :
						pat = re.compile(reg)
						choice = pat.split(allChoices)
						choices = ""
						countChoice = 0
						for x in choice :
							x = x.strip()
							if len(x) > 1 :
								countChoice += 1
								choices += u'##' + x
						choices += u"##"
						if countChoice > 1 :
							break
					# print choices
					
					# Get description from each problem
					ind = pro.index(allChoices)
					description = pro[0 : ind]
					description = description.strip()
				else :
					choices = u"##正确##错误##"
					description = pro
					# 题目描述已经处理，因为判断题无选项字段需要去除
				
				# 去除题目序号
				# 实际不需要？分开题目时已经去除？
				pat = re.compile(app.config['REGEX_PROBLEM_INDEX'])
				des = pat.match(description)
				
				try :
					des = des.group()
					description = description[len(des):]
				except Exception as e :
					description = description
				
				ret.append((description, choices, answer))
			except MyOperateError as e :
				print e.description
				# raise MyOperateError(u'Unexpected Error.')
			except Exception as e :
				print e
				print u'Unexpected Error.'
				# raise MyOperateError(u'Unexpected Error.')
		
		return ret


def addSessionTempFile(x) :
	if 'tempfile' in session :
		session.pop('tempfile', None)
	session['tempfile'] = x
	print session
		
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
					raise MyOperateError('The number of problems is too small.')
				
				
				# print 'fine'
				
				if current_user.isAdmin == True :
					doc = models.Document(title = title, author = current_user, subjectId = category)
					db.session.add(doc)
					for content, choices, answer in format_content :
						pro = models.Problem(source = doc, content = content, choice = choices, answer = answer)
						db.session.add(pro)
					db.session.commit()
					flash(app.config['SUCCESS_UPLOAD'])
					return redirect(url_for('processProblems.show', 
									did = unicode(doc.id)))
				else :
					doc = models.Document(title = title, author = current_user, subjectId = category)
					db.session.add(doc)
					for content, choices, answer in format_content :
						pro = models.Problem(source = doc, content = content, choice = choices, answer = answer)
						db.session.add(pro)
					db.session.commit()
					
					addSessionTempFile(doc.id)
					# print session
					# print title
					# print 'session:', session['tempfile'][0]
					flash(app.config['SUCCESS_PROCESS'])
					return redirect(url_for('processProblems.show', 
									did = unicode(6666666)))
			except MyOperateError as e:
				print '\n\n\n xxx :', e.description
				print '\r\n\r\n\r\n\r\n\r\n\r\n\r\n\n'
				flash(app.config['FAIL_PROCESS'] + '1')
			except Exception as e:
				print '\n\n\n yyy :', e
				print '\r\n\r\n\r\n\r\n\r\n\r\n\r\n\n'
				flash(app.config['FAIL_PROCESS'] + '2')
		else :
			if current_user.isAdmin :
				flash(app.config['FAIL_UPLOAD'])
			else :
				flash(app.config['FAIL_PROCESS'] + '3')
	return render_template('processProblems/upload.html', form = form)