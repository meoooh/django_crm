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
