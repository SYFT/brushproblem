# -*- coding: utf-8 -*-

CSRF_ENABLED = True
SECRET_KEY = '123456'

from datetime import timedelta
REMEMBER_COOKIE_DURATION = timedelta(days = 1)

import os
baseDir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(baseDir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(baseDir, 'db_repository')


UPLOAD_FOLDER = os.path.join(baseDir, 'uploads_files')
UPLOADS_DEFAULT_DEST  = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = ('txt', 'pdf', 'doc', 'docx')
MAX_CONTENT_LENGTH = 8 * 1024 * 1024

WHOOSH_BASE = os.path.join(baseDir, 'whoosh_index')

TIMEDELTA_CHOICE = [(0, u'今天'), 
			(1, u'一星期内'),
			(2, u'一月内（30天）'), 
			(3, u'无限制')]
TIMEDELTA = [timedelta(days = 1),
			timedelta(days = 7),
			timedelta(days = 30),
			timedelta(days = 4000)]
DEFAULT_TIME_DELTA = 3

CHOICE_INDEX = u'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

MESSAGE_FOR_RIGHT = u'Your are right!'
MESSAGE_FOR_WRONG = u'Your are wrong! Right answer is %s.'

PASSWROD_NOT_MATCH = u'Old password do not match!'
