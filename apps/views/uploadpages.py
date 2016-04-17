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

class FileOperateError :
	description = ""

	def __init__(self, description = "Wrong in file!"):
		self.description = description
	
	def __repr__(self):
		return self.description
	

@uploadpages.route('/upload', methods = ['GET', 'POST'])
@login_required
def upload() :
	form = UploadForm()
	if request.method == 'POST' :
#		print "here"
		try :
#			print "hello"
#			title = us.save(request.files['problem'])
#			print "say"
#			flash("The title of the file has been changed to " + title + ".")
#			flash(u'It\'s now checking...Please wait for it.')
			
			f = request.files[form.file.name]
			tmp = str(f.filename)
			tmp = tmp.split('.')
			if len(tmp) < 2:
				raise FileOperateError(u'Filename is illegal!')
			
			title = tmp[0]
			extendsion = tmp[1]
			if form.filename.data :
				title = form.filename.data
			print title

			p = models.Problem(title = title, author = current_user)
			print f.filename
			print 'xx' + f.filename
			
			ntitle = us.save(f)
			flash(ntitle)

			folder = os.path.join(app.config['UPLOAD_FOLDER'], "us")
			turner = app.config['TURNER_NAME'];
			_compile = 'java -classpath ' + folder + ' ' + turner
			_args = ntitle + ' ' + str(p.id) + '.txt'
			commands = _compile + ' ' + _args
			
			print commands
			proc = subprocess.Popen(commands, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			startTime = time.time()
			print startTime
			while proc.poll() is None :
				endTime = time.time()
				if endTime - startTime > 3000 :
					print endTime
					proc.kill()
			
			if proc.poll() == 1 :
				raise FileOperateError();	
			
			stdout, stderr = proc.communicate()
			if len(stderr) > 0:
				raise FileOperateError(u'Some wrong in file format.')
			output_status = stdout.split(' ')
			if output_status[0] == '1' :
				raise FileOperatorError(output_status[1])
			
			flash(u'Succefully receive!!!')
			
			# if the subprocess is not finish yet, x.poll() is a None
			# else x.poll() return a int
			# if the subprocess finish and stop as normal, it return 0
			# else it return 1 represents that some wrongs interrupt it or you kill it
		except FileOperateError as e:
			print e
			flash(u'Sorry, this file is not allow to upload !!')
		except Exception as e:
			print e
			flash(u'Sorry, this file is not allow to upload !!')
	return render_template('uploadpages/upload.html', form = form)
