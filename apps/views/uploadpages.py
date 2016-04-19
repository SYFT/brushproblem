from flask import Flask, request, session, \
					g, redirect, url_for, \
					abort, render_template, flash,  \
					Blueprint
from apps.forms import UploadForm
from flask.ext.login import login_required, current_user
from apps import lm, db, models, us, app
import subprocess, os, time

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
	problems = x.split('\n')
	

@uploadpages.route('/upload', methods = ['GET', 'POST'])
@login_required
def upload() :
	form = UploadForm()
	if request.method == 'POST' :
#		print "here"
		try :
			title = form.filename.data
			content = form.file.data
#			category = form
			format_content = change(content)
#			format_content should be a pair list
#			the first element should be problem's description
#			the second element should be problem's answer
			doc = models.Document(title = title, author = g.user, category = category)
			db.session.add(doc)
			for content, answer in format_content :
				pro = models.Document(source = doc, content = content, answer = answer)
				db.session.add(pro)
			db.session.commit()
		except MyOperateError as e:
			print e
			flash(u'Sorry, this file is not allow to upload !!')
		except Exception as e:
			print e
			flash(u'Sorry, this file is not allow to upload !!')
	return render_template('uploadpages/upload.html', form = form)
