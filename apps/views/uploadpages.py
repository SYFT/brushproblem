# -*- coding: utf-8 -*-

from flask import Flask, request, session, \
					g, redirect, url_for, \
					abort, render_template, flash,  \
					Blueprint
from apps.forms import UploadForm
from flask.ext.login import login_required, current_user
from apps import lm, db, models, us, app
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
	
def change(x) :
	problems = x.split(u'\r\n\r\n')
	print problems
	ret = []
	for p in problems :
		pro = p
		
		try :
		
			# Set the first letter in pro to be the answer
			# Get Answer from each problem
			pat = re.compile(u'[\(,（]+[A-Z]+[\),）]+')
			answer = pat.search(pro)
			if answer is None :
				raise MyOperateError(u'No Answer in brackets.')
			answer = answer.group()
			print answer
			
			pat = re.compile(u'[\(,（,\),）]')
			ans = pat.split(answer)
			answer = ''
			for i in range(0, len(ans)) :
				ans[i] = ans[i].strip()
				if len(ans[i]) > 0 :
					answer += ans[i]
			
			print 'answer:', answer
			pat = re.compile(u'[\(,（]+[A-Z]+[\),）]+')
			pro = pat.subn('____', pro)
			pro = pro[0]
			print 'pro:', pro
			
			# Get choices
			# Choices must be set in the tail of the problem
			pat = re.compile(u'[A-Z][\.,、]+.*', re.S)
			allChoices = pat.search(pro)
			allChoices = allChoices.group()
			print 'allchoices:', allChoices
			pat = re.compile(u'[ ,\r,\n,A-Z,、,，,\,.]+')
			choice = pat.split(allChoices)
			choices = ""
			for x in choice :
				x = x.strip()
				if len(x) > 0 :
					choices += u'##' + x
			choices += u"##"
			
			# Get description from each problem
			ind = pro.index(allChoices)
			description = pro[0 : ind]
			description = description.strip()
			pat = re.compile(u'[0-9,\.,、]*')
			des = pat.match(description)
			des = des.group()
			description = description[len(des):]
			
			ret.append((description, choices, answer))
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
	
	if 'form' in dir() :
		print 'hhhhhhh'
		print form.validate_on_submit()
		print form.subject.data
		print form.subject.choices
		print form.filename.data
		print form.file.data
		print request.method
		print form.errors
	if request.method == 'POST' and form.validate_on_submit() :
		print "here"
		try :
			
			title = form.filename.data
			content = form.file.data
			category = form.subject.data
			
			format_content = change(content)
#			format_content should be a pair list
#			the first element should be problem's description
#			the second element should be problem's answer
			
			print format_content
			for x, y, z in format_content :
				print x.encode('gb2312'), y.encode('gb2312'), z.encode('gb2312')
			
			if len(format_content) < 2 :
				raise MyOperateError('The number of problems is too small.')
			doc = models.Document(title = title, author = current_user, subjectId = category)
			db.session.add(doc)
			for content, choices, answer in format_content :
				pro = models.Problem(source = doc, content = content, choice = choices, answer = answer)
				db.session.add(pro)
			db.session.commit()
			flash(u'Successfully uploaded!')
		except MyOperateError as e:
			print e
			flash(u'Sorry, this file is not allow to upload !!')
		except Exception as e:
			print e
			flash(u'Sorry, this file is not allow to upload !!')
	else :
		flash(u'Upload failed!')
	return render_template('uploadpages/upload.html', form = form)
