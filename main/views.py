# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def index(request):
	return render(request, 'index.html')

def base(request):
	return render(request, 'base.html')

def list(request):
	return render(request, 'moviegrid.html')

def login_site(request):
	if request.method == 'POST':
		username = request.POST['email']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user:
			login(request, user)
			return redirect('/index/')
		else:
			context = {}
			context['error'] = "Wrong Credentials"
			return render(request, 'login.html',context)
	else:
		if request.user.is_authenticated():
			return redirect
		context = {}
		context['error'] = ''
		return render(request,'login.html', context)

def register(request):
	if request.method == 'POST':
		firstName = request.POST['fname']
		lastName = request.POST['lname']
		username = request.POST['email']
		password = request.POST['password']
		user = User.objects.create(
				username = username,
				first_name = firstName,
				last_name = lastName
			)
		user.set_password(password)
		user.save()
		user = authenticate(username=username, password=password)
		if user is not None:
		 	login(request, user)
		# 	profile=Profile.objects.create(
		# 			user=user,
		# 			firstName=firstName,
		# 			lastName=lastName,
		# 			username=username,
		# 			regDate=timezone.now(),
		# 		)
		return redirect('/index/')
	else:
		return render(request, 'register.html')

def logout_site(request):
	logout(request)
	return redirect('/index/')
