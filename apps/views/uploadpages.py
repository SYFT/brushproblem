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

@uploadpages.route('/upload', method = ['GET', 'POST'])
@login_required
def upload() :
	form = UploadForm()
	if request.method == 'POST' and form.file.data :
		title = us.save(request.FILES[form.file.name])
		reccd ddd
	return render_template('uploadpages/upload.html', form = form)
