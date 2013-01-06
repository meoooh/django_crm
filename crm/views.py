# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

@login_required
def mainPage(request):
	variables = RequestContext(request, {
			'username': request.user.username,
			})
	
	return render_to_response('mainPage.html', variables)

def userRegister(request):
#	if request.user.is_authenticated(): #로그인 여부 검사
#		return HttpResponseRedirect('/')
#로그인 중에도 회원가입 가능하게 해야할지...
	if request.method == 'POST':
		form = userRegisterationForm(request.POST)
		
		if form.is_valid():
			user = User.objects.create_user(
					username=form.cleaned_data['userId'],
					password=form.cleaned_data['password1'],
					email=form.cleaned_data['email'],
					)
			user=user.getprofile()
			user.name=form.cleaned_data['userName']
			user.mobile=form.cleaned_data['mobile']

			return HttpResponseRedirect('/')
	elif request.method == 'GET':
		form = userRegisterationForm()
	else:
		return HttpResponseRedirect('/userRegisteration/')
		# 로깅 할 필요 있음. 구현 후 추가 예정.
	
	variables = RequestContext(request, {
		'form':form,
		})
	return render_to_response('/registeration/userRegisteration.html',
		variables,
		)
