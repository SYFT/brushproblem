# -*- coding: utf-8 -*-

CSRF_ENABLED = True
SECRET_KEY = '123456'

from datetime import timedelta
REMEMBER_COOKIE_DURATION = timedelta(days = 1)

import os
baseDir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(baseDir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(baseDir, 'db_repository')


# UPLOAD_FOLDER = os.path.join(baseDir, 'uploads_files')
# UPLOADS_DEFAULT_DEST  = UPLOAD_FOLDER
# ALLOWED_EXTENSIONS = ('txt', 'pdf', 'doc', 'docx')
# MAX_CONTENT_LENGTH = 8 * 1024 * 1024

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

# 优先括号内的内容
# 其次是行末的字母或者×√两种符号
# 然后是最后一个‘对’或者‘错’的标识
# 最后是最后一个字母
# 判断题特别的答案 ×√╳xX
REGEX_ANSWER = (u'[\(（][A-Za-z ×√╳\uff21-\uff3a\uff41-\uff5a]+[\)）]',
				u'[A-Za-z×√╳\uff21-\uff3a\uff41-\uff5a]+ *[\r\n]+',
				u'[对错]+',
				u'[A-Za-z×√╳\uff21-\uff3a\uff41-\uff5a]+')
RIGHT_ANSWER = u'对√'
WRONG_ANSWER = u'错xX╳×'
REGEX_CHOICE = (u'[A-Z\uff21-\uff3a][\.,、,．]+.*',
				u'[A-Z\uff21-\uff3a].*')
REGEX_CHOICE_INDEX = u'[A-Z\uff21-\uff3a]+[\.,、,．]|\r\n'
REGEX_PROBLEM_INDEX = u'[0-9]+[\.,、,．]'

MESSAGE_FOR_RIGHT = u'Your are right!'
MESSAGE_FOR_WRONG = u'Your are wrong! Right answer is %s.'

PASSWROD_NOT_MATCH = u'Old password do not match!'

LOGIN_MESSAGE = u'Please login first.'
# flash while access some login_required pages
# without login
REFRESH_MESSAGE = (u"To protect your account, please reauthenticate to access this page.")
# a list of message that will flash while 
SUCCESS_LOGIN = u'成功登入！'
SUCCESS_UPLOAD = u'成功上传！'
SUCCESS_PROCESS = u'成功处理！'
FAIL_LOGIN = u'登入失败！'
FAIL_UPLOAD = u'上传失败！'
FAIL_PROCESS = u'处理异常！'