from flask import Flask, request, session, \
					g, redirect, url_for, \
					abort, render_template, flash,  \
					Blueprint
from apps.forms import UploadForm
from flask.ext.login import login_required
from apps import lm, db, models, us

uploadpages = Blueprint('uploadpages', __name__, 
					static_folder = 'static',
					template_folder = 'templates')

@uploadpages.route('/upload', methods = ['GET', 'POST'])
@login_required
def upload() :
	form = UploadForm()
	if request.method == 'POST' :
		print "here"
		#form = UploadForm(request.POST)
		#if form.file.data :
		try :
			title = us.save(request.files['problem'])
			flash("The title of the file has been changed to " + title + ".")
			flash(u'It\'s now checking...Please wait for it.')
		except Exception as e:
			print e
			flash(u'Sorry, this file is not allow to upload !!')
	return render_template('uploadpages/upload.html', form = form)
