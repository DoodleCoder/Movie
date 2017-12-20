# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, JsonResponse
import json
import urllib.request
from django.shortcuts import render, get_object_or_404, redirect
from django.core.cache import cache
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt


api = '4a95b57fbcd4eea6c3e07a72ee861599'
lang = 'en-US'
genreURL = 'https://api.themoviedb.org/3/genre/movie/list?api_key='+api+'&language='+lang
response0 = urllib.request.urlopen(genreURL)
genre = json.loads(response0.read())
genre = genre['genres']


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
			profile=Profile.objects.create(
					user=user,
					firstName=firstName,
					lastName=lastName,
					username=username,
				)
			seenlist = Seenlist.objects.create(
					user=user
				)
			watchlist = Watchlist.objects.create(
					user=user
				)
			return redirect('/index/')
	else:
		return render(request, 'register.html')

def logout_site(request):
	logout(request)
	return redirect('/index/')

def index(request):
	popmovie = cache.get('popmovie')
	nowmovie = cache.get('nowmovie')
	topmovie = cache.get('topmovie')
	upmovie = cache.get('upmovie')
	if not popmovie:
		popmovie= []
		popurl = 'https://api.themoviedb.org/3/movie/popular?api_key='+api+'&language='+lang+'&page=1'
		response0 = urllib.request.urlopen(popurl)
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



	if not nowmovie:
		nowmovie=[]
		nowurl= 'https://api.themoviedb.org/3/movie/now_playing?api_key='+api+'&language='+lang+'&page=1'
		response0 = urllib.request.urlopen(nowurl)
		now = json.loads(response0.read())
		for i in now['results']:
			i['genres']=[]
			for j in genre:
				if j['id'] in i['genre_ids']:
					i['genres'].append(j['name'])	
		nowmovie.append(now['results'])
		cache.set('nowmovie', nowmovie, 18000)  #18000 here is the number of seconds until the caache clears this data
		print('NEW ENTRY')
	else:
		print('old entry')


	if not topmovie:
		topmovie=[]
		topurl= 'https://api.themoviedb.org/3/movie/top_rated?api_key='+api+'&language='+lang+'&page=1'
		response0 = urllib.request.urlopen(topurl)
		top = json.loads(response0.read())
		for i in top['results']:
			i['genres']=[]
			for j in genre:
				if j['id'] in i['genre_ids']:
					i['genres'].append(j['name'])	
		topmovie.append(top['results'])
		cache.set('topmovie', topmovie, 18000)  #18000 here is the number of seconds until the caache clears this data	
		print('NEW ENTRY')
	else:
		print('old entry')


	if not upmovie:
		upmovie=[]
		upurl= 'https://api.themoviedb.org/3/movie/upcoming?api_key='+api+'&language='+lang+'&page=1'
		response0 = urllib.request.urlopen(upurl)
		up = json.loads(response0.read())
		for i in up['results']:
			i['genres']=[]
			for j in genre:
				if j['id'] in i['genre_ids']:
					i['genres'].append(j['name'])	
		upmovie.append(up['results'])
		cache.set('upmovie', upmovie, 18000)
		print('NEW ENTRY')
	else:
		print('old entry')



	airtodayshow = cache.get('lateshow')
	airshow = cache.get('airshow')
	popshow = cache.get('popshow')
	topshow = cache.get('topshow')
	
	if not airtodayshow:
		airtodayshow= []
		airtodayurl = 'https://api.themoviedb.org/3/tv/airing_today?api_key='+api+'&language='+lang+'&page=1'
		response0 = urllib.request.urlopen(airtodayurl)
		airtoday = json.loads(response0.read())
		for i in airtoday['results']:
			i['genres']=[]
			for j in genre:
				if j['id'] in i['genre_ids']:
					i['genres'].append(j['name'])	
		airtodayshow.append(airtoday['results'])
		cache.set('airtodayshow', airtodayshow, 18000)  #18000 here is the number of seconds until the caache clears this data
		print('NEW ENTRY')
	else:
		print('old entry')


	if not airshow:
		airshow=[]
		airurl= 'https://api.themoviedb.org/3/tv/on_the_air?api_key='+api+'&language='+lang+'&page=1'
		response0 = urllib.request.urlopen(airurl)
		air = json.loads(response0.read())
		for i in air['results']:
			i['genres']=[]
			for j in genre:
				if j['id'] in i['genre_ids']:
					i['genres'].append(j['name'])	
		airshow.append(air['results'])
		cache.set('airshow', airshow, 18000)  #18000 here is the number of seconds until the caache clears this data
		print('NEW ENTRY')
	else:
		print('old entry')


	if not popshow:
		popshow=[]
		popurl= 'https://api.themoviedb.org/3/tv/popular?api_key='+api+'&language='+lang+'&page=1'
		response0 = urllib.request.urlopen(popurl)
		pop = json.loads(response0.read())
		for i in pop['results']:
			i['genres']=[]
			for j in genre:
				if j['id'] in i['genre_ids']:
					i['genres'].append(j['name'])	
		popshow.append(pop['results'])
		cache.set('popshow', popshow, 18000)
		print('NEW ENTRY')
	else:
		print('old entry')


	if not topshow:
		topshow=[]
		topurl= 'https://api.themoviedb.org/3/tv/top_rated?api_key='+api+'&language='+lang+'&page=1'
		response0 = urllib.request.urlopen(topurl)
		top = json.loads(response0.read())
		for i in top['results']:
			i['genres']=[]
			for j in genre:
				if j['id'] in i['genre_ids']:
					i['genres'].append(j['name'])	
		topshow.append(top['results'])
		cache.set('topshow', topshow, 18000)  #18000 here is the number of seconds until the caache clears this data	

	context={
		'pop': popmovie,
		'now': nowmovie,
		'top': topmovie,
		'up': upmovie,
		'airtoday': airtodayshow,
		'air': airshow,
		'popular': popshow,
		'toprate': topshow,
	}
	return render(request, 'index.html', context)

def base(request):
	return render(request, 'base.html')

def movielist(request):
	if request.user.is_authenticated():		
		popmovie = cache.get('popmovie')	#find in cache
		if not popmovie:					#if not in cache, call api
			popmovie= []
			for i in range(1,11):			#ignore this part
				popurl = 'https://api.themoviedb.org/3/movie/popular?api_key='+api+'&language='+lang+'&page='+str(i) #develop the api
				response0 = urllib.request.urlopen(popurl) 	#call the api
				pop = json.loads(response0.read())	#
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

def movie(request, movie_id):
	movurl = 'https://api.themoviedb.org/3/movie/'+movie_id+'?api_key='+api+'&language='+lang+'&page=1'
	response0 = urllib.request.urlopen(movurl)
	mov = json.loads(response0.read())
	date=mov['release_date']
	date=date[:4]

	movcredurl= 'https://api.themoviedb.org/3/movie/'+movie_id+'/credits?api_key='+api+'&language='+lang+'&page=1'
	response0 = urllib.request.urlopen(movcredurl)
	movcred = json.loads(response0.read())
	cast=movcred['cast']
	crew=movcred['crew']
	writers=[]
	producers=[]
	for c in crew:
		if(c['job']=='Director'):
			director=c
		elif(c['department']=='Writing'):
			writers.append(c)
		elif(c['department']=='Production'):
			producers.append(c)

	movsimurl='https://api.themoviedb.org/3/movie/'+movie_id+'/similar?api_key='+api+'&language='+lang+'&page=1'
	response0 = urllib.request.urlopen(movsimurl)
	movsim = json.loads(response0.read())
	movsim=movsim['results']

	movrevurl='https://api.themoviedb.org/3/movie/'+movie_id+'/reviews?api_key='+api+'&language='+lang+'&page=1'
	response0 = urllib.request.urlopen(movrevurl)
	movrev = json.loads(response0.read())
	movrev=movrev['results']

	context={
		'detail':mov,
		'date':date,
		'cast':cast,
		'casto':cast[:7],
		'crew':crew,
		'director':director,
		'writers':writers,
		'producers':producers,
		'movsim':movsim,
		'reviews':movrev,
	}
	return render(request, 'moviesingle.html',context)

def show(request, show_id):
	showurl = 'https://api.themoviedb.org/3/tv/'+show_id+'?api_key='+api+'&language='+lang
	response0 = urllib.request.urlopen(showurl)
	showdet = json.loads(response0.read())
	date=showdet['first_air_date']
	date=date[:4]
	if(showdet['in_production']):
		enddate='current'
	else:
		enddate=showdet['last_air_date']
		enddate=enddate[:4]
	seasons=showdet['seasons']
	curr=seasons[-1]

	showsimurl= 'https://api.themoviedb.org/3/tv/'+show_id+'/similar?api_key='+api+'&language='+lang+'&page=1'
	response0 = urllib.request.urlopen(showsimurl)
	showsim = json.loads(response0.read())
	showsim=showsim['results']

	showcredurl= 'https://api.themoviedb.org/3/tv/'+show_id+'/credits?api_key='+api+'&language='+lang+'&page=1'
	response0 = urllib.request.urlopen(showcredurl)
	showcred = json.loads(response0.read())
	cast=showcred['cast']
	crew=showcred['crew']
	writers=[]
	producers=[]
	director=""
	for c in crew:
		if(c['job']=='Director'):
			director=c
		elif(c['department']=='Writing'):
			writers.append(c)
		elif(c['department']=='Production'):
			producers.append(c)

	showkeyurl='https://api.themoviedb.org/3/tv/'+show_id+'/keywords?api_key='+api+'&language='+lang+'&page=1'
	response0 = urllib.request.urlopen(showkeyurl)
	showkey = json.loads(response0.read())
	keywords=showkey['results']

	context={
		'detail':showdet,
		'showsim':showsim,
		'director':director,
		'writers':writers,
		'producers':producers,
		'cast':cast,
		'date': date,
		'enddate': enddate,
		'curr':curr,
		'keywords':keywords,
	}
	return render(request, 'seriessingle.html', context)

def tvlist(request):
	if request.user.is_authenticated():		
		poptv = cache.get('poptv')
		if not poptv:
			poptv= []
			for i in range(1,11):
				popurl = 'https://api.themoviedb.org/3/tv/popular?api_key='+api+'&language='+lang+'&page='+str(i)
				response0 = urllib.urlopen(popurl)
				pop = json.loads(response0.read())
				for i in pop['results']:
					i['genres']=[]
					for j in genre:
						if j['id'] in i['genre_ids']:
							i['genres'].append(j['name'])	
				poptv.append(pop['results'])
			cache.set('poptv', poptv, 18000)
			print('NEW ENTRY')
		else:
			print('old entry')

		context={
			'poptv': poptv,
		}
		return render(request, 'tvgrid.html', context)
	else:
		return redirect('/login/')

@csrf_exempt
def search(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			query = request.POST['query']
			t = request.POST['search-type']
			print(query,  t)
			if t=='movie':
				s_movies = cache.get(str(query)+t)
				if not s_movies: 
					url = 'https://api.themoviedb.org/3/search/movie?api_key='+api+'&language='+lang+'&query='+query+'&page=1&include_adult=false'
					response = urllib.urlopen(url)
					s_movies = json.loads(response.read())['results']
					cache.set(str(query)+t, s_movies, 18000)
				context = {
					'results' : s_movies,
					's' : query,
					't' : t,
				}
			else:
				s_tv = cache.get(str(query)+t)
				if not s_tv: 
					url = 'https://api.themoviedb.org/3/search/tv?api_key='+api+'&language='+lang+'&query='+query+'&page=1'
					response = urllib.urlopen(url)
					s_tv = json.loads(response.read())['results']
					cache.set(str(query)+t, s_tv, 18000)
				context = {
					'results' : s_tv,
					's' : query,
					't' : t,
				}

			return render(request, 'search.html', context)
		else:
			return HttpResponse('Not Allowed')
	else:
		return redirect('/login/')