from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
	user = models.ForeignKey(User, unique=True)
	mobile = models.CharField(unique=True, max_length=11)
	lastIp= models.GenericIPAddressField()
	position = models.CharField(max_length=10)
	function = models.CharField(max_length=10)
	level = models.CharField(max_length=10)
	team = models.CharField(max_length=20)
	name = models.CharField(max_length=70)
