# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.contrib.auth.views import login
from django.contrib.auth import logout
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from crm.forms import *
from crm.models import *

@login_required
def mainPage(request):
	variables = RequestContext(request, {
			'user': request.user,
			})
	
	return render_to_response('mainPage.html', variables)

def userRegistration(request):
#	if request.user.is_authenticated(): #로그인 여부 검사
#		return HttpResponseRedirect('/')
#로그인 중에도 회원가입 가능하게 해야할지...
	if request.method == 'POST':
		form = userRegistrationForm(request.POST)
		
		if form.is_valid():
			user = User.objects.create_user(
					username=form.cleaned_data['userId'],
					password=form.cleaned_data['password1'],
					email=form.cleaned_data['email'],
					)
			UserProfile.objects.create(user=user)
			# get_profile관련 https://docs.djangoproject.com/en/dev/topics/auth/customizing/#auth-profiles
			# http://www.turnkeylinux.org/blog/django-profile
			# http://stackoverflow.com/questions/5477925/django-1-3-userprofile-matching-query-does-not-exist
			user=user.get_profile()
#			import pdb
#			pdb.set_trace()
			user.name=form.cleaned_data['userName']
			user.mobile=form.cleaned_data['mobile']

			user.save()

			return HttpResponseRedirect('/')
	elif request.method == 'GET':
		form = userRegistrationForm()
	else:
		return HttpResponseRedirect('/userRegistration/')
		# 로깅 할 필요 있음. 구현 후 추가 예정.
	
	variables = RequestContext(request, {
		'form':form,
		})
	return render_to_response('registration/userRegistration.html',
		variables,
		)

def logoutPage(request):
	logout(request) # from django.contrib.auth import logout

	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	# from django.http import HttpResponseRedirect

def loginPage(request):
	loginReturnValue=login(request=request)

	if request.method == 'POST' and request.user.is_authenticated():
		user = request.user.get_profile()
		user.lastIp = request.META.get('REMOTE_ADDR')
		user.save()
	
	return loginReturnValue

@login_required
def workDailyRecord(request, mode_name):
	form = WorkDailyRecordForm()
	if request.method == 'GET':
		if mode_name == u'edit/':
			workDailyRecord = WorkDailyRecord.objects.get(pk=request.GET['pk'])
			target_user = ', '.join(
					w.get_profile().name for w in workDailyRecord.target_user.all()
					)
			form = WorkDailyRecordForm({
#				'ongoing_or_end':workDailyRecord.ongoing_or_end,
				'contents':workDailyRecord.contents,
				'target_user':target_user,
			})
			
			variables = RequestContext(request, {
				'form':form,
			})
			
			return render_to_response('workDailyRecordForm.html', variables)
		elif mode_name == None:
			workDailyRecord = WorkDailyRecord.objects.order_by('date')
		
#		import pdb
#		pdb.set_trace()
		variables = RequestContext(request, {
					'user':request.user,
					'form':form,
					'workDailyRecord':workDailyRecord,
				})

		return render_to_response('workDailyRecord.html', variables)
	elif request.method == 'POST':
#		import pdb
#		pdb.set_trace()
		#form = WorkDailyRecordForm(request.POST)
		ajax = request.GET.has_key('ajax')
		if mode_name == u'del/':
			if ajax:
				workDailyRecord = WorkDailyRecord.objects.get(pk=request.POST['pk'])
				workDailyRecord.delete()
				return HttpResponse('1')	 # from django.http import HttpResponse
		elif mode_name == None:
			if ajax:
				if request.POST.has_key('pk'): #수정
					if request.GET.has_key('edit'):
						workDailyRecord = WorkDailyRecord.objects.get(pk=request.POST['pk'])
						workDailyRecord.contents = request.POST['contents']
#						workDailyRecord.ongoing_or_end = request.POST['ongoing_or_end']
						
						workDailyRecord.target_user.clear()
						
						target_users = request.POST['target_user'].split(',')
					
						for target_user in target_users:
							user=''
							target_user=target_user.strip()
							try:
								user = UserProfile.objects.get(name=target_user).user
							except ObjectDoesNotExist:
								continue
							workDailyRecord.target_user.add(user)
						
						workDailyRecord.save()
					elif request.GET.has_key('check'):
						workDailyRecord = WorkDailyRecord.objects.get(pk=request.POST['pk'])
						
						workDailyRecord.check_user.add(request.user)
						workDailyRecord.save()
						
						return HttpResponse('1')
					elif request.GET.has_key('uncheck'):
						workDailyRecord = WorkDailyRecord.objects.get(pk=request.POST['pk'])
						
						workDailyRecord.check_user.remove(request.user)
						workDailyRecord.save()
						
						return HttpResponse('1')
					elif request.GET.has_key('ongoing'):
#						import pdb;pdb.set_trace()
						workDailyRecord = WorkDailyRecord.objects.get(pk=request.POST['pk'])
						
						workDailyRecord.ongoing_or_end = u'ing';
						workDailyRecord.save()
						
#						return HttpResponse('1')
					elif request.GET.has_key('end'):
#						import pdb;pdb.set_trace()
						workDailyRecord = WorkDailyRecord.objects.get(pk=request.POST['pk'])
						
						workDailyRecord.ongoing_or_end = u'end';
						workDailyRecord.save()
						
#						return HttpResponse('1')
				else:
					workDailyRecord = WorkDailyRecord.objects.create(
						user=request.user,
						contents=request.POST['contents'],
#						ongoing_or_end=request.POST['ongoing_or_end'],
					)
					
					target_users = request.POST['target_user'].split(',')
				
					for target_user in target_users:
						user=''
						target_user=target_user.strip()
						try:
							user = UserProfile.objects.get(name=target_user).user
						except ObjectDoesNotExist:
							continue
						workDailyRecord.target_user.add(user)
						workDailyRecord.save()
					
				variables = RequestContext(request, {
						'form':form,
						'workDailyRecord':[workDailyRecord],
					})	
					
				return render_to_response('onlyWorkDailyRecord.html', variables)
			else:
				workDailyRecord = WorkDailyRecord.objects.create(
					user=request.user,
					contents=request.POST['contents'],
#					ongoing_or_end=request.POST['ongoing_or_end'],
				)
				
				target_users = request.POST['target_user'].split(',')
				
				for target_user in target_users:
					user=''
					target_user=target_user.strip()
					try:
						user = UserProfile.objects.get(name=target_user).user
					except ObjectDoesNotExist:
						continue
					workDailyRecord.target_user.add(user)
					workDailyRecord.save()
				
				return HttpResponseRedirect('/workDailyRecord/')
				
@login_required
def searchUser(request):
	if request.GET.has_key('q'):
		users = UserProfile.objects.filter(name__istartswith=request.GET['q'])
		
		return HttpResponse('\n'.join(user.name for user in users))
	return HttpResponse()