from flask import Flask, request, session, \
					g, redirect, url_for, \
					abort, render_template, flash,  \
					Blueprint
from apps.forms import UploadForm
from flask.ext.login import login_required
from apps import lm, db, models, us, app
import subprocess, os, time

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
			folder = os.path.join(app.config['UPLOAD_FOLDER'], "us")
			turner = os.path.join(folder, app.config['TURNER_NAME'])
			print turner
			foutput = open(os.path.join(folder, 'xxx.txt'), 'w')

			timebegin = time.time()
			x = subprocess.Popen(turner, stdout = foutput, shell = True)
			while x.poll() is None :
				timenow = time.time()
				if timenow - timebegin > 1000 :
					x.kill()
			if x.poll() == 0 :
				flash(u'Succefully receive!!')
			else :
				flash(u'Unsuccefully receive')
			print x.poll()
		except Exception as e:
			print e
			flash(u'Sorry, this file is not allow to upload !!')
	return render_template('uploadpages/upload.html', form = form)
