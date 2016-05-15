# -*- coding: utf-8 -*-
from apps import app, db, models
from apps.forms import SearchProblemForm, ProblemForm, \
						BrushForm, ChoiceForm, UploadForm
from apps.models import MyOperateError
import re

def myValidate(arrayForm) :
	for pro in arrayForm :
		if not pro.validate_on_submit() :
			return False
		for choice in pro.choices :
			if not choice.validate_on_submit() :
				return False
	return True

def getAllProblem(doc) :
	allProblem = BrushForm()
	allProblem.pro = []
	count = 0
	allProblem.title = doc.title
	for x in doc.problems :
		count += 1
		# description = str(count) + u'、' + x.content.title()
		# Use ol/li to index the problems
		description = x.content.title()
		choices = x.choice.split(u'##')
		# print 'x.choice:', x.choice
		# print 'x.answer:', x.answer
		countChoice = 0
		pro = ProblemForm()
		pro.choices = []
		for y in choices :
			y = y.strip()
			if len(y) > 0 :
				option = chr(countChoice + ord('A'))
				choicesDescription = \
					option + \
					u'、' + unicode(y)
				
				thisChoice = ChoiceForm()
				thisChoice.option.default = False
				thisChoice.option.name = unicode(count)
				thisChoice.option.id = unicode(count)
				thisChoice.option.userValue = option
				thisChoice.description = unicode(choicesDescription)
				pro.choices.append(thisChoice)
				countChoice += 1
		try :
			pro.pid = x.id
			realPro = models.Problem.query.filter(models.Problem.id == pro.pid)
			realPro = realPro.first()
			pro.realAnswer = unicode(realPro.answer)
		except Exception as e :
			pro.realAnswer = x.answer
		pro.index = count
		pro.description = description
		pro.check = 0
		allProblem.pro.append(pro)
	return allProblem

def change(x, documentType = 0) :
	# 0 -> 答案在括号中     1 -> 答案在全文最后
	if documentType == 0 :
		x = x.replace(unicode(chr(63)), u'_')
		pat = re.compile(u'\r\n *[0-9]+[\.、,．､]|保险. ')
		problems = pat.split(x)
		# print problems
		ret = []
		for pro in problems :
			# print 'pro:', pro[0:24]
			if len(pro) < 3 :
				continue
			
			try :
				panDuanTi = False
				# Set the first letter in pro to be the answer
				# Get Answer from each problem
				getAnswer = False
				for reg in app.config['REGEX_ANSWER'] :
					pat = re.compile(reg)
					ansMatch = pat.search(pro)
					if ansMatch is None :
						print 'hi'
						continue
					
					while True :
						next = pat.search(pro, ansMatch.end())
						if next is None :
							break
						ansMatch = next
						# print ansMatch.start()
					
					answer = ansMatch.group()
					answer = answer.strip()
					
					pat = re.compile(u'[\(（\)）  ]')
					ans = pat.split(answer)
					answer = ''
					for i in range(0, len(ans)) :
						ans[i] = ans[i].strip()
						if len(ans[i]) > 0 :
							answer += ans[i]
					# print answer
					if len(answer) < 1 :
						continue
					getAnswer = True
					
					if answer in app.config['RIGHT_ANSWER'] or \
						answer in app.config['WRONG_ANSWER'] :
						if answer in app.config['RIGHT_ANSWER'] :
							answer = u'A'
						else :
							answer = u'B'
						panDuanTi = True
					
					# print pro
					answerSpace = u'___'
					pat = re.compile(u'_')
					tmp = pat.search(pro)
					if tmp is None :
						answerSpace = u'___'
					else :
						answerSpace = u''
					pro = pro[:ansMatch.start()] + answerSpace + pro[ansMatch.end():]
					
					break
				
				if getAnswer == False :
					# print '\r\n\r\n Wrong here:', pro
					# print '\r\n\r\n unicode here:', pro.decode('utf8')
					
					for reg in app.config['REGEX_ANSWER'] :
						pat = re.compile(reg)
						answer = pat.search(pro)
						# print answer
					raise MyOperateError(u'No Answer in brackets.')
				
				# print 'hhh'
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
					for reg in app.config['REGEX_CHOICE_INDEX'] :
						pat = re.compile(reg)
						choice = pat.split(allChoices)
						choices = ""
						countChoice = 0
						for x in choice :
							x = x.strip()
							if len(x) > 1 :
								countChoice += 1
								choices += u'##' + x
						choices += u"##"
						if countChoice > 1 :
							break
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
				# raise MyOperateError(u'Unexpected Error.')
			except Exception as e :
				print e
				print u'Unexpected Error.'
				# raise MyOperateError(u'Unexpected Error.')
		
		return ret