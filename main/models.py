# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Profile(models.Model):
	user= models.ForeignKey(User)
	firstName = models.CharField(max_length=100, default='')
	lastName = models.CharField(max_length=100, default='')
	username = models.CharField(max_length=100, default='')
	country = models.CharField(max_length=100, default='')
	def __str__(self):
		return str(self.id) + '-' + self.user.username + ' Profile'

