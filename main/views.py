# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, JsonResponse
import urllib, json
from django.shortcuts import render, get_object_or_404, redirect
from django.core.cache import cache
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout

# Create your views here.

api = '4a95b57fbcd4eea6c3e07a72ee861599'
lang = 'en-US'
genreURL = 'https://api.themoviedb.org/3/genre/movie/list?api_key='+api+'&language='+lang
response0 = urllib.urlopen(genreURL)
genre = json.loads(response0.read())
genre = genre['genres']
# print(genre)

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

def index(request):
	return render(request, 'index.html')

def base(request):
	return render(request, 'base.html')

def movielist(request):
	if request.user.is_authenticated():		
		popmovie = cache.get('popmovie')
		if not popmovie:
			popmovie= []
			for i in range(1,11):
				popurl = 'https://api.themoviedb.org/3/movie/popular?api_key='+api+'&language='+lang+'&page='+str(i)
				response0 = urllib.urlopen(popurl)
				pop = json.loads(response0.read())
				for i in pop['results']:
					i['genres']=[]
					for j in genre:
						if j['id'] in i['genre_ids']:
							i['genres'].append(j['name'])	
				popmovie.append(pop['results'])
			cache.set('popmovie', popmovie, 18000)  #18000 here is the number of seconds until the caache clears this data
			print('NEW ENTRY')
		else:
			print('old entry')
		context={
			'pop': popmovie,
		}
		return render(request, 'moviegrid.html', context)
	else:
		return redirect('/login/')

def search(request):
	pass