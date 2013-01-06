# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.contrib.auth import logout
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from crm.forms import *
from crm.models import *

@login_required
def mainPage(request):
	variables = RequestContext(request, {
			'username': request.user.username,
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
			_user=UserProfile.objects.create(user=user)
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
