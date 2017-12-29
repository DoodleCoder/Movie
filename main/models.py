# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
	user= models.ForeignKey(User)
	firstName = models.CharField(max_length=100, default='')
	lastName = models.CharField(max_length=100, default='')
	username = models.CharField(max_length=100, default='')
	country = models.CharField(max_length=100, default='')
	def __str__(self):
		return str(self.id) + '-' + self.user.username + ' Profile'

class Movie(models.Model):
	user = models.ForeignKey(User)
	name = models.CharField(max_length=1000)
	m_id = models.IntegerField()
	w_add = models.IntegerField(default=0)
	s_add = models.IntegerField(default=0)
	d_rating = models.IntegerField(default=0)
	date = models.CharField(max_length=9999)
	overview = models.TextField()
	pic = models.CharField(max_length=9999)
	def __str__(self):
		return str(self.name)

class Watchlist(models.Model):
	movie = models.ForeignKey(Movie)
	user = models.ForeignKey(User, default='')
	def __str__(self):
		return str(self.user.username)+'-'+str(self.movie.name)

class Seenlist(models.Model):
	movie = models.ForeignKey(Movie)
	user = models.ForeignKey(User, default='')
	rate = models.IntegerField(default=0)
	def __str__(self):
		return str(self.user.username)

class Genre(models.Model):
	user = models.ForeignKey(User)
	name = models.CharField(max_length=1000) 
	def __str__(self):
		return str(self.name)
