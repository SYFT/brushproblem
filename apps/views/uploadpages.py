# -*- coding: utf-8 -*-

from flask import Flask, request, session, \
					g, redirect, url_for, \
					abort, render_template, flash,  \
					Blueprint
from apps.forms import UploadForm
from flask.ext.login import login_required, current_user
from apps import lm, db, models, app
import subprocess, os, time, re

uploadpages = Blueprint('uploadpages', __name__, 
					static_folder = 'static',
					template_folder = 'templates')

class MyOperateError(Exception) :
	description = ""

	def __init__(self, description = "Wrong in file!"):
		self.description = description
	
	def __repr__(self):
		return self.description
	
def change(x, documentType = 0) :
	# 0 -> 答案在括号中     1 -> 答案在全文最后
	if documentType == 0 :
		pat = re.compile(u'\r\n *[0-9]+[\.,、,．]')
		problems = pat.split(x)
		# print problems
		ret = []
		for pro in problems :
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
						continue
					getAnswer = True
					
					while True :
						next = pat.search(pro, ansMatch.end())
						if next is None :
							break
						ansMatch = next
					
					answer = ansMatch.group()
					answer = answer.strip()
					# print answer
					
					pat = re.compile(u'[\(（\)） ]')
					ans = pat.split(answer)
					answer = ''
					for i in range(0, len(ans)) :
						ans[i] = ans[i].strip()
						if len(ans[i]) > 0 :
							answer += ans[i]
					# print 'answer:', answer
					
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
					print '\r\n\r\n Wrong here:', pro
					print '\r\n\r\n unicode here:', pro.decode('utf8')
					
					for reg in app.config['REGEX_ANSWER'] :
						pat = re.compile(reg)
						answer = pat.search(pro)
						print answer
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
					pat = re.compile(app.config['REGEX_CHOICE_INDEX'])
					choice = pat.split(allChoices)
					choices = ""
					for x in choice :
						x = x.strip()
						if len(x) > 0 :
							choices += u'##' + x
					choices += u"##"
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
				raise MyOperateError(u'Unexpected Error.')
			except Exception as e :
				print e
				raise MyOperateError(u'Unexpected Error.')
		
		return ret


@uploadpages.route('/upload', methods = ['GET', 'POST'])
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
				content = form.file.data
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
				else :
					flash(app.config['SUCCESS_PROCESS'])
					session['tempfile'] = models.Tempfile(title = title, pros = format_content)
					return redirect(url_for('viewproblems.show', did = 100))
			except MyOperateError as e:
				print '\n\n\n xxx :', e.description
				flash(app.config['FAIL_PROCESS'])
			except Exception as e:
				print '\n\n\n yyy :', e
				flash(app.config['FAIL_PROCESS'])
		else :
			if current_user.isAdmin :
				flash(app.config['FAIL_UPLOAD'])
			else :
				flash(app.config['FAIL_PROCESS'])
	return render_template('uploadpages/upload.html', form = form)
