# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.views.generic import TodayArchiveView, DayArchiveView, MonthArchiveView, YearArchiveView, ListView, DetailView
from django.contrib.auth.views import login
from django.contrib.auth import logout
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404
from crm.forms import *
from crm.models import *
from datetime import date, datetime, timedelta
from django.core.urlresolvers import reverse
from crm.utility import *

import iptools

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

	return HttpResponseRedirect("/")
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
#			import pdb;pdb.set_trace()
			try:
				return TodayLogView.as_view()(request)
			except Http404:
#				workDailyRecord = WorkDailyRecord.objects.filter(ongoing_or_end=date.today)
				pass
			else:
				return render_to_response('test.html')
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
				# import pdb;pdb.set_trace()
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
				# import ipdb;ipdb.set_trace()
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

class TodayLogView(TodayArchiveView):
	"""
	https://gist.github.com/4579130
	http://ccbv.co.uk/projects/Django/1.4/django.views.generic.dates/TodayArchiveView/
	"""
	model = WorkDailyRecord #임포트 한 모델 클래스 명을 적어 줍니다.
	context_object_name = 'workDailyRecord' # 템플릿에서 쓸 때 필요합니다.
	date_field = 'date'
#	month_format = '%m' # 달을 숫자[01-12]형태로 표현합니다.
	template_name = "workDailyRecord.html"
#	allow_empty = True
	
	def get_context_data(self, **kwargs): # WorkDailyRecordForm()을 template에 전달하기 위해서
		context = super(TodayLogView, self).get_context_data(**kwargs)
		context['form'] = WorkDailyRecordForm()
#		import pdb;pdb.set_trace()
		return context
		
class DailyLogView(DayArchiveView):
	model = WorkDailyRecord 
	context_object_name = 'workDailyRecord'
	date_field = 'date'
	month_format = '%m'
	template_name = "workDailyRecord.html"
	allow_empty = True
  
	def get_context_data(self, **kwargs): # WorkDailyRecordForm()을 template에 전달하기 위해서
		context = super(DayArchiveView, self).get_context_data(**kwargs)
		context['form'] = WorkDailyRecordForm()
#		import pdb;pdb.set_trace()
		return context
		
class MonthlyLogView(MonthArchiveView):
	model = WorkDailyRecord 
	context_object_name = 'workDailyRecord'
	date_field = 'date'
	month_format = '%m'
	template_name = "workDailyRecord.html"
	allow_empty = True
  
	def get_context_data(self, **kwargs): # WorkDailyRecordForm()을 template에 전달하기 위해서
		context = super(MonthArchiveView, self).get_context_data(**kwargs)
		context['form'] = WorkDailyRecordForm()
#		import pdb;pdb.set_trace()
		return context
		
class YearlyLogView(YearArchiveView):
	model = WorkDailyRecord 
	context_object_name = 'workDailyRecord'
	date_field = 'date'
#	year_format = '%Y'
	template_name = "workDailyRecord.html"
	allow_empty = True
  
	def get_context_data(self, **kwargs): # WorkDailyRecordForm()을 template에 전달하기 위해서
		context = super(YearArchiveView, self).get_context_data(**kwargs)
		context['form'] = WorkDailyRecordForm()
#		import pdb;pdb.set_trace()
		return context
		
	
def customer(request):
	if request.method == "GET":
		form = CustomerRegistrationForm()
		
	variables = RequestContext(request, {
					'form':form,
				})

	return render_to_response('customer.html', variables)
		
def customerRegistration(request):
	if request.method == "GET":
		form = CustomerRegistrationForm()
	elif request.method == "POST":
		# import pdb;pdb.set_trace()
		form = CustomerRegistrationForm(request.POST)
		
		if form.is_valid():
			customer = Customer.objects.create(
				name=form.cleaned_data['name'],
				position=form.cleaned_data['position'],
				serviceName=form.cleaned_data['serviceName'],
				detailedServiceName=form.cleaned_data['detailedServiceName'],
				serviceNumber=form.cleaned_data['serviceNumber'],
				dataFolder=form.cleaned_data['dataFolder'],
			)
		
			personInCharge, created = PersonInCharge.objects.get_or_create(
				name=form.cleaned_data['personInChargesName'],
				telephone1=form.cleaned_data['personInChargesTel'],
				mobile1=form.cleaned_data['personInChargesMobile'],
				email1=form.cleaned_data['personInChargesEmail'],
			)
			customer.personInCharges.add(personInCharge)
			
			worker = UserProfile.objects.get(name=form.cleaned_data['workers']).user
			customer.workers.add(worker)
			
			salesperson = UserProfile.objects.get(name=form.cleaned_data['salespersons']).user
			customer.salespersons.add(salesperson)
			
			for i in form.cleaned_data['ipaddrs'].split(','):
				if iptools.validate_cidr(i.strip()):
					for j in iptools.IpRange(i.strip()):
						ipaddr, created=IPaddr.objects.get_or_create(
							addr=j,
						)
#						ipaddr.country=GeoIP(j)
						note = Note(
							content_object=ipaddr,
							contents=form.cleaned_data['ipaddrsNote'],
							writer=request.user,
						)
						note.save()
						customer.ipaddrs.add(ipaddr)
				elif iptools.validate_ip(i.strip()):
					for j in iptools.IpRange(i.strip()):
						ipaddr, created=IPaddr.objects.get_or_create(
							addr=j,
						)
#						ipaddr.country=GeoIP(j)
						note = Note(
							content_object=ipaddr,
							contents=form.cleaned_data['ipaddrsNote'],
							writer=request.user,
						)
						note.save()
						customer.ipaddrs.add(ipaddr)
			
			for i in form.cleaned_data['domains'].split(','):
				domain, created= Domain.objects.get_or_create(
					url=i,
				)
				note = Note(
							content_object=domain,
							contents=form.cleaned_data['domainsNote'],
							writer=request.user,
						)
				note.save()
				customer.domains.add(domain)
				
			ipaddr, created=IPaddr.objects.get_or_create(
				addr=form.cleaned_data['equipmentsIpaddr'],
			)
			#ipaddr.country=GeoIP(j)
			equipment, created = Equipment.objects.get_or_create(
				ipaddr=ipaddr
			)
			equipment.type=form.cleaned_data['equipmentsType']
			equipment.save()
			note = Note(
				content_object=equipment,
				contents=form.cleaned_data['equipmentsNote'],
				writer=request.user,
			)
			note.save()
			customer.equipments.add(equipment)
			
			for i in form.cleaned_data['alertEmails'].split(','):
				# import pdb;pdb.set_trace()
				personInCharge, created = PersonInCharge.objects.get_or_create(
					email1=i,
				)
				if created:
					personInCharge.name=customer.name+u' 담당자'
					personInCharge.save()
				customer.alertEmails.add(personInCharge)
				
			for i in form.cleaned_data['alertSMSs'].split(','):
				personInCharge, created = PersonInCharge.objects.get_or_create(
					mobile1=i,
				)
				if created:
					personInCharge.name=customer.name+u' 담당자'
					personInCharge.save()
				customer.alertSMSs.add(personInCharge)
				
			customer.save()
			return HttpResponseRedirect(reverse('customer')) # from django.core.urlresolvers import reverse
		
	variables = RequestContext(request, {
					'form':form,
				})

	return render_to_response('customerRegistration.html', variables)
	
class customerList(ListView):
	model = Customer 
	context_object_name = 'customerList'
	template_name = "customer.html"
	allow_empty = True
	
class customerDetailView(DetailView):
	context_object_name = 'customerDetail'
	template_name = "customerDetail.html"
	allow_empty = True
	model = Customer
	slug_field = 'name'