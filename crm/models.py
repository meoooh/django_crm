# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class UserProfile(models.Model):
	user = models.ForeignKey(User, unique=True) # OneToOneField으로 바꿔야함 생각을 잘못했음...
	mobile = models.CharField(unique=True, max_length=11)
	lastIp= models.GenericIPAddressField(null=True)
	position = models.CharField(max_length=10, null=True)
	function = models.CharField(max_length=10, null=True)
	level = models.CharField(max_length=10, null=True)
	team = models.CharField(max_length=20, null=True)
	name = models.CharField(max_length=70)

	def __unicode__(self):
		return '%s, %s, %s, %s, %s, %s, %s, %s'%(
				self.user.username, 
				self.name,
				self.mobile, 
				self.lastIp, 
				self.position, 
				self.function, 
				self.level, 
				self.team, 
			)

class WorkDailyRecord(models.Model):
	user = models.ForeignKey(User)
	date = models.DateTimeField(auto_now_add=True)
	contents = models.TextField()
	check_user = models.ManyToManyField(
				User,
				related_name='checked_user_record_set',
			)
	target_user = models.ManyToManyField(
				User,
				related_name='target_user_record_set',
			)

	ONGOING_OR_END =(
				('ing', '진행중'),
				('end', '완료'),
			)


	ongoing_or_end = models.CharField(
				max_length=3,
				choices=ONGOING_OR_END,
				default='ing',
			)

	def __unicode__(self):
		return '%s, %s, %s, check_user: %s, target_user: %s, ongoing_or_end: %s'%(
					self.user.get_profile().name,
					self.date,
					self.contents,
					self.check_user.all(),
					self.target_user.all(),
					self.ongoing_or_end,
				)
	
class Note(models.Model):
	contents = models.TextField()
	writer = models.ForeignKey(User)
	date = models.DateTimeField(auto_now_add=True)
	
	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()
	content_object = generic.GenericForeignKey('content_type', 'object_id')

	def __unicode__(self):
		return "writer: %s, content: %s, date: %s"%(self.writer.get_profile().name, self.content, self.date)
	
class IPaddr(models.Model):
	notes = generic.GenericRelation(Note, null=True)
	addr = models.GenericIPAddressField(unique=True,)
	country = models.CharField(max_length=30, null=True)
	
class PersonInCharge(models.Model):
	name = models.CharField(max_length=50,)
	telephone1 = models.CharField(null=True, max_length=20)
	telephone2 = models.CharField(null=True, max_length=20)
	mobile1 = models.CharField(null=True, max_length=20)
	mobile2 = models.CharField(null=True, max_length=20)
	email1 = models.EmailField(null=True)
	email2 = models.EmailField(null=True)
	notes = generic.GenericRelation(Note, null=True)
	
class Domain(models.Model):
	url = models.URLField(unique=True,)
	notes = generic.GenericRelation(Note, null=True)
	
class Equipment(models.Model):
	types =(
				('ids', 'IDS'),
				('ips', 'IPS'),
				('fw', '방화벽'),
				('waf', '웹방화벽'),
				('SW', '스위치'),
				('ddos', 'Anti-DDos'),
				('log', 'Log'),
				('utm', 'UTM'),
				('etc', '기타'),
			)
	
	type = models.CharField(
				choices=types,
				default='etc',
				max_length=4,
			)
	ipaddr = models.ForeignKey(IPaddr, null=True)
	notes = generic.GenericRelation(Note, null=True)
	
class Customer(models.Model):
	name = models.CharField(max_length=50,)
	personInCharges = models.ManyToManyField(PersonInCharge, null=True, related_name='customer_personincharges_personincharge_set')
	position = models.CharField(null=True, max_length=50,)
	serviceName = models.CharField(null=True, max_length=50,)
	detailedServiceName = models.CharField(null=True, max_length=50,)
	serviceNumber = models.CharField(null=True, max_length=50,)
	dataFolder = models.CharField(null=True, max_length=50,)
	workers = models.ManyToManyField(User, related_name='customer_workers_user_set', null=True)
	salespersons = models.ManyToManyField(User, related_name='customer_salespersons_user_set', null=True)
	notes = generic.GenericRelation(Note, null=True)
	ipaddrs = models.ManyToManyField(IPaddr, related_name='customer_ipaddrs_ipaddr_set', null=True)
	domains = models.ManyToManyField(Domain, related_name='customer_domains_domain_set', null=True)
	equipments = models.ManyToManyField(Equipment, related_name='customer_equipment_set', null=True)
	alertEmails = models.ManyToManyField(PersonInCharge, related_name='customer_alertEmails_personincharge_set', null=True)
	alertSMSs = models.ManyToManyField(PersonInCharge, related_name='customer_alertSMSs_personincharge_set', null=True)
	date = models.DateTimeField(auto_now_add=True)