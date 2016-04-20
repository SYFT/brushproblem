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

TURNER_NAME = 'documentchange'