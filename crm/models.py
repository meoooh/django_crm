# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
	user = models.ForeignKey(User, unique=True)
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
	date = models.DateTimeField(auto_now=True)
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
