# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, JsonResponse
import json
import urllib
from operator import itemgetter
from django.shortcuts import render, get_object_or_404, redirect
from django.core.cache import cache
from django.contrib.auth.models import User
from .models import Profile, Genre, Movie, Watchlist, Seenlist
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt


api = '4a95b57fbcd4eea6c3e07a72ee861599'
lang = 'en-US'
genreURL = 'https://api.themoviedb.org/3/genre/movie/list?api_key='+api+'&language='+lang
response0 = urllib.urlopen(genreURL)
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
	popmovie = cache.get('popmovie-index')
	nowmovie = cache.get('nowmovie')
	topmovie = cache.get('topmovie')
	upmovie = cache.get('upmovie')
	if not popmovie:
		popmovie= []
		popurl = 'https://api.themoviedb.org/3/movie/popular?api_key='+api+'&language='+lang+'&page=1'
		response0 = urllib.urlopen(popurl)
		pop = json.loads(response0.read())
		for i in pop['results']:
			i['genres']=[]
			for j in genre:
				if j['id'] in i['genre_ids']:
					i['genres'].append(j['name'])	
		popmovie.append(pop['results'])
		cache.set('popmovie-index', popmovie, 18000)  #18000 here is the number of seconds until the caache clears this data
		print('NEW ENTRY')
	else:
		print('old entry')



	if not nowmovie:
		nowmovie=[]
		nowurl= 'https://api.themoviedb.org/3/movie/now_playing?api_key='+api+'&language='+lang+'&page=1'
		response0 = urllib.urlopen(nowurl)
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
		response0 = urllib.urlopen(topurl)
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
		response0 = urllib.urlopen(upurl)
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
		response0 = urllib.urlopen(airtodayurl)
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
		response0 = urllib.urlopen(airurl)
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
		response0 = urllib.urlopen(popurl)
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
		response0 = urllib.urlopen(topurl)
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

def movielist(request,page_no):
	pageNo=int(page_no)
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
					popmovie.append(i)
			cache.set('popmovie', popmovie, 18000)  
		poplist=popmovie
		print(popmovie)
		pop = sorted(poplist, key=itemgetter('popularity'), reverse=True)
		if request.method == 'POST':	
			t = request.POST['filter']
			rate = sorted(poplist, key=itemgetter('vote_average'), reverse=True)
			a_z = sorted(poplist, key=itemgetter('title'))
			z_a = sorted(poplist, key=itemgetter('title'), reverse=True)
			date = sorted(poplist, key=itemgetter('release_date'), reverse=True)
			if t == '1':
				context={
					'results': pop[(pageNo-1)*20:pageNo*20],
					't' : t,
				}
			elif t == '2':
				context={
					'results': rate[(pageNo-1)*20:pageNo*20],
					't' : t,
				}
			elif t == '3':
				context={
					'results': date[(pageNo-1)*20:pageNo*20],
					't' : t,
				}
			elif t == '4':
				context={
					'results' : a_z[(pageNo-1)*20:pageNo*20],
					't' : t,
				}
			elif t == '5':
				context={
					'results' : z_a[(pageNo-1)*20:pageNo*20],
					't' : t,
				}
			else:
				context={
					'results' : pop[(pageNo-1)*20:pageNo*20],
					't' : t,
				}
		else:
			context={
				'results' : pop[(pageNo-1)*20:pageNo*20],
				't' : 1,
			}
		context['page']=pageNo
		context['pageNumbers']=[1,2,3,4,5,6,7,8,9,10]
		return render(request, 'moviegrid.html', context)
	else:
		return redirect('/login/')

def movie(request, movie_id):
	mov = cache.get('movie-'+str(movie_id))
	if not mov:
		movurl = 'https://api.themoviedb.org/3/movie/'+movie_id+'?api_key='+api+'&language='+lang+'&page=1'
		response0 = urllib.urlopen(movurl)
		mov = json.loads(response0.read())
		cache.set('movie-'+str(movie_id), mov)
		print('NEW ENTRY')
	else:
		print('old entry')
	date=mov['release_date']
	date=date[:4]
	r = int(mov['vote_average'])
	q = int(10-r)
	ratingsss = [i for i in range(r)]
	# print(ratingsss)
	non_ratingsss = [i for i in range(q)]


	movcred = cache.get('movie-'+str(movie_id)+'-cred')
	if not movcred:
		movcredurl= 'https://api.themoviedb.org/3/movie/'+movie_id+'/credits?api_key='+api+'&language='+lang+'&page=1'
		response0 = urllib.urlopen(movcredurl)
		movcred = json.loads(response0.read())
		cache.set('movie-'+str(movie_id)+'-cred', movcred)
		print('NEW ENTRY')
	else:
		print('old entry')		
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

	movsim = cache.get('movie-'+str(movie_id)+'-sim')
	if not movsim:
		movsimurl='https://api.themoviedb.org/3/movie/'+movie_id+'/similar?api_key='+api+'&language='+lang+'&page=1'
		response0 = urllib.urlopen(movsimurl)
		movsim = json.loads(response0.read())
		movsim=movsim['results']
		cache.set('movie-'+str(movie_id)+'-sim', movsim)
		print('NEW ENTRY')
	else:
		print('old entry')

	movrev = cache.get('movie-'+str(movie_id)+'-review')
	if not movrev:
		movrevurl='https://api.themoviedb.org/3/movie/'+movie_id+'/reviews?api_key='+api+'&language='+lang+'&page=1'
		response0 = urllib.urlopen(movrevurl)
		movrev = json.loads(response0.read())
		movrev=movrev['results']
		cache.set('movie-'+str(movie_id)+'-review', movrev)
		print('NEW ENTRY')
	else:
		print('old entry')

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
		'abcdef':ratingsss,
		'uvwxyz':non_ratingsss,
	}
	m = Movie.objects.get_or_create(
			name=mov['title'],
			m_id=movie_id,
			d_rating = mov['vote_average'],
			pic='https://image.tmdb.org/t/p/w500'+mov['poster_path'],
			overview=mov['overview'],
			date=mov['release_date'][:4]
		)
	for g in mov['genres']:
			gen = Genre.objects.get_or_create(
				user=request.user,
				name=g['name']
			)
	return render(request, 'moviesingle.html',context)

def show(request, show_id):
	showdet = cache.get('tv-'+str(show_id))
	if not showdet:
		showurl = 'https://api.themoviedb.org/3/tv/'+show_id+'?api_key='+api+'&language='+lang
		response0 = urllib.urlopen(showurl)
		showdet = json.loads(response0.read())
		cache.set('tv-'+str(show_id), showdet)
		print('NEW ENTRY')
	else:
		print('old entry')

	date=showdet['first_air_date']
	date=date[:4]
	if(showdet['in_production']):
		enddate='current'
	else:
		enddate=showdet['last_air_date']
		enddate=enddate[:4]
	seasons=showdet['seasons']
	curr=seasons[-1]

	showsim = cache.get('tv-'+str(show_id)+'-sim')
	if not showsim:
		showsimurl= 'https://api.themoviedb.org/3/tv/'+show_id+'/similar?api_key='+api+'&language='+lang+'&page=1'
		response0 = urllib.urlopen(showsimurl)
		showsim = json.loads(response0.read())
		showsim=showsim['results']
		cache.set('tv-'+str(show_id)+'-sim', showsim)
		print('NEW ENTRY')
	else:
		print('old entry')

	showcred = cache.get('tv-'+str(show_id)+'-cred')
	if not showcred:
		showcredurl= 'https://api.themoviedb.org/3/tv/'+show_id+'/credits?api_key='+api+'&language='+lang+'&page=1'
		response0 = urllib.urlopen(showcredurl)
		showcred = json.loads(response0.read())
		cache.set('tv-'+str(show_id)+'-cred',showcred)
		print('NEW ENTRY')
	else:
		print('old entry')
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

	showkey = cache.get('tv-'+str(show_id)+'-keywords')
	if not showkey:
		showkeyurl='https://api.themoviedb.org/3/tv/'+show_id+'/keywords?api_key='+api+'&language='+lang+'&page=1'
		response0 = urllib.urlopen(showkeyurl)
		showkey = json.loads(response0.read())
		keywords=showkey['results']
		cache.set('tv-'+str(show_id)+'-keywords', showkey)
		print('NEW ENTRY')
	else:
		print('old entry')

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

@csrf_exempt
def add_watchlist(request, movie_id):
	# print('reached')
	user = request.user
	m = Movie.objects.get(m_id=movie_id)
	if m.s_add == 0:
		if m.w_add == 0:
			m.w_add = 1
			m.save()
			w = Watchlist.objects.create(
					user=user,
					movie=m,
				)
			w.save();
			return JsonResponse({
				'success': 'true'
				})
		else:
			return JsonResponse({
				'success': 'false-already in watchlist'
				})
	else:
		return JsonResponse({
			'success' : 'false-already in seenlist'
			})

@csrf_exempt
def add_seenlist(request, movie_id):
	# print('reached')
	t = json.loads(request.body.decode('utf-8'))
	print(t)
	rate = t['u_rate']
	user = request.user
	m = Movie.objects.get(m_id=movie_id)
	if m.w_add == 0:
		if m.s_add == 0:
			m.s_add = 1
			m.u_rating = rate
			m.save()
			s = Seenlist.objects.create(
					user=user,
					movie=m,
				)
			s.save();
			return JsonResponse({
				'success': 'true'
				})
		else:
			return JsonResponse({
				'success': 'false-already in seenlist'
				})
	else:
		return JsonResponse({
			'success': 'false-already in watchlist'
			})

def seen(request):
	seens=Seenlist.objects.filter(user=request.user)
	a = []
	for i in seens:
		a.append(i.movie)
	context={
		'seenMovies':a,
	}
	return render(request, 'seenlist.html', context)

def watch(request):
	watch=Watchlist.objects.filter(user=request.user)
	a = []
	for i in watch:
		a.append(i.movie)
	context={
		'watchMovies':a,
	}
	return render(request, 'watchlist.html', context)

def profile(request):
	pro=Profile.objects.get(user=request.user)
	print(pro)
	user=User.objects.get(id=request.user.id)
	if request.method == 'POST':
		print('hi')
		username=request.POST['username']
		fname=request.POST['fname']
		lname=request.POST['lname']
		country=request.POST['country']

		pro.username=username
		pro.firstName=fname
		pro.lastName=lname
		pro.country=country
		pro.save()
		user.first_name=fname
		user.last_name=lname
		user.username=username
		user.save()

	context={
		'profile': pro
	}
	return render(request, 'profile.html', context)		

