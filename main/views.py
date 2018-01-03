# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, JsonResponse
import json
import urllib
from operator import itemgetter
from django.shortcuts import render, get_object_or_404, redirect
from django.core.cache import cache
from django.contrib.auth.models import User
from .models import Profile, Genre, Movie, Watchlist, Seenlist, TV, WatchlistTV, SeenlistTV
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from dateutil.parser import parse
from django.core.files.storage import FileSystemStorage


api = '4a95b57fbcd4eea6c3e07a72ee861599'
lang = 'en-US'
genreURL = 'https://api.themoviedb.org/3/genre/movie/list?api_key='+api+'&language='+lang
response0 = urllib.urlopen(genreURL)
genre = json.loads(response0.read())
genre = genre['genres']
gid=[28,12,16,35,80,99,18,10751,14,36,27,10402,9648,10749,878,10770,53,10752,37]
gname = ['Action','Adventure','Animation','Comedy','Crime','Documentary','Drama','Family','Fantasy','History','Horror','Music','Mystery','Romance','Science Fiction','TV Movie','Thriller','War','Western']
idsss=[i for i in range(19)]

def populate_movies():
	popmovie = cache.get('popmovie')	
	if not popmovie:					
		popmovie= []
		for i in range(1,201):
			popurl = 'https://api.themoviedb.org/3/movie/upcoming?api_key='+api+'&language='+lang+'&page='+str(i) 
			response0 = urllib.urlopen(popurl) 	
			pop = json.loads(response0.read())	
			for i in pop['results']:
				i['genres']=[]
				for j in genre:
					if j['id'] in i['genre_ids']:
						i['genres'].append(j['name'])	
				popmovie.append(i)
		for i in range(201,401):
			popurl = 'https://api.themoviedb.org/3/movie/upcoming?api_key='+api+'&language='+lang+'&page='+str(i) 
			response0 = urllib.urlopen(popurl) 	
			pop = json.loads(response0.read())	
			for i in pop['results']:
				i['genres']=[]
				for j in genre:
					if j['id'] in i['genre_ids']:
						i['genres'].append(j['name'])	
				popmovie.append(i)
		for i in range(401,601):
			popurl = 'https://api.themoviedb.org/3/movie/upcoming?api_key='+api+'&language='+lang+'&page='+str(i) 
			response0 = urllib.urlopen(popurl) 	
			pop = json.loads(response0.read())	
			for i in pop['results']:
				i['genres']=[]
				for j in genre:
					if j['id'] in i['genre_ids']:
						i['genres'].append(j['name'])	
				popmovie.append(i)
		cache.set('popmovie', popmovie, 18000) 
	c=popmovie
	fp = open('allmovies.txt', 'a')
	for i in c:
		try:
			fp.write(str(i['id'])+'|'+(i['title'])+'|')
		except UnicodeEncodeError:
			continue
		ge = [0 for j in range(19)]
		l = i['genre_ids']
		for k in range(19):
			if gid[k] in l:
				ge[k] = 1
			else: 
				ge[k]=0
		for i in ge:
			fp.write(str(i)+'|')
		fp.write('\n')
	fp.close()

def populate_ratings():
	fp = open('ratings.txt','w')
	usersAll = User.objects.all()
	for u in usersAll:
		seenAll = Seenlist.objects.filter(user=u)
		for s in seenAll:
			fp.write(str(u.id)+'|'+str(s.movie.m_id)+'|'+str(s.rate)+'\n')
			# print(s.movie.name,s.rate)
	fp.close()

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
			return redirect('/index/')
	else:
		return render(request, 'register.html')

def logout_site(request):
	logout(request)
	return redirect('/index/')

def index(request):
	popmovie = cache.get('popmovie-index')
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
		popmovie.append(pop['results'][:10])
		cache.set('popmovie-index', popmovie, 18000)  #18000 here is the number of seconds until the caache clears this data
		print('NEW ENTRY')
	else:
		print('old entry')


	nowmovie = cache.get('nowmovie')
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
		nowmovie.append(now['results'][:10])
		cache.set('nowmovie', nowmovie, 18000)  #18000 here is the number of seconds until the caache clears this data
		print('NEW ENTRY')
	else:
		print('old entry')


	topmovie = cache.get('topmovie')
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
		topmovie.append(top['results'][:10])
		cache.set('topmovie', topmovie, 18000)  #18000 here is the number of seconds until the caache clears this data	
		print('NEW ENTRY')
	else:
		print('old entry')


	upmovie = cache.get('upmovie')
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
		upmovie.append(up['results'][:10])
		cache.set('upmovie', upmovie, 18000)
		print('NEW ENTRY')
	else:
		print('old entry')



	airtodayshow = cache.get('lateshow')
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
		airtodayshow.append(airtoday['results'][:10])
		cache.set('airtodayshow', airtodayshow, 18000)  #18000 here is the number of seconds until the caache clears this data
		print('NEW ENTRY')
	else:
		print('old entry')


	airshow = cache.get('airshow')
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
		airshow.append(air['results'][:10])
		cache.set('airshow', airshow, 18000)  #18000 here is the number of seconds until the caache clears this data
		print('NEW ENTRY')
	else:
		print('old entry')


	popshow = cache.get('popshow')
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
		popshow.append(pop['results'][:10])
		cache.set('popshow', popshow, 18000)
		print('NEW ENTRY')
	else:
		print('old entry')


	topshow = cache.get('topshow')
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
		topshow.append(top['results'][:10])
		cache.set('topshow', topshow, 18000)  #18000 here is the number of seconds until the caache clears this data	
	print(len(popmovie))
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

def tvlist(request,page_no):
	pageNo=int(page_no)
	g=''
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
					poptv.append(i)
			cache.set('poptv', poptv, 18000)  
		poplist=poptv
		pop = sorted(poplist, key=itemgetter('popularity'), reverse=True)
		if request.method == 'POST':	
			t = request.POST['filter']
			rate = sorted(poplist, key=itemgetter('vote_average'), reverse=True)
			a_z = sorted(poplist, key=itemgetter('name'))
			z_a = sorted(poplist, key=itemgetter('name'), reverse=True)
			date = sorted(poplist, key=itemgetter('first_air_date'), reverse=True)
			if t == '1':
				results = pop[(pageNo-1)*20:pageNo*20]
				context={
					
					'results': pop[(pageNo-1)*20:pageNo*20],
					't' : t,
				}
			elif t == '2':
				results = rate[(pageNo-1)*20:pageNo*20]
				context={
					
					'results': results,
					't' : t,
				}
			elif t == '3':
				results = date[(pageNo-1)*20:pageNo*20]
				context={
					
					'results': results,
					't' : t,
				}
			elif t == '4':
				results = a_z[(pageNo-1)*20:pageNo*20]
				context={
						
					'results' : results,
					't' : t,
				}
			elif t == '5':
				results = z_a[(pageNo-1)*20:pageNo*20]
				context={
						
					'results' : results,
					't' : t,
				}
			else:
				results = pop[(pageNo-1)*20:pageNo*20]
				context={
						
					'results' : results,
					't' : t,
				}
			context['page']=pageNo
			tpages = int(len(results)/20)+1
			context['pageNumbers']=[i for i in range(1,tpages+1)]
			context['tpages']=tpages
			return render(request, 'tvgrid.html', context)
		else:
			name = request.GET.get('name','')
			g = request.GET.getlist('g','')
			r = request.GET.get('r','')
			ans = []
			for i in poplist:
				if name.lower() in i['name'].lower():
					ans.append(i)
			ans2 = []
			
			if g != '[]' or g!= '':
				for i in ans:
					b=0
					for j in g:
						if j in i['genres']:
							b+=1
					if b == len(g):
						ans2.append(i)
			else:
				g = ''
				ans2 = ans
			results = []
			if r=='6-10':
				for i in ans2:
					if i['vote_average'] > 6:
						results.append(i)
			elif r=='3-6':
				for i in ans2:
					if i['vote_average'] > 3 and i['vote_average'] < 6:
						results.append(i)
			elif r=='0-3':
				for i in ans2:
					if i['vote_average'] < 3:
						results.append(i)
			else:
				results = ans2
			context={
					'results' : results[(pageNo-1)*20:pageNo*20],
					't' : '1',
				}
			context['page']=pageNo
			context['string'] = name
			context['genress'] = g
			context['ratingss'] = r
			tpages = int(len(results)/20)+1
			context['pageNumbers']=[i for i in range(1,tpages+1)]
			context['tpages']=tpages
			return render(request, 'tvgrid.html', context)

	else:
		return redirect('/login/')

def movielist(request,page_no):
	pageNo=int(page_no)
	g=''
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
		pop = sorted(poplist, key=itemgetter('popularity'), reverse=True)
		if request.method == 'POST':	
			t = request.POST['filter']
			rate = sorted(poplist, key=itemgetter('vote_average'), reverse=True)
			a_z = sorted(poplist, key=itemgetter('title'))
			z_a = sorted(poplist, key=itemgetter('title'), reverse=True)
			date = sorted(poplist, key=itemgetter('release_date'), reverse=True)
			if t == '1':
				results = pop[(pageNo-1)*20:pageNo*20]
				context={
					
					'results': pop[(pageNo-1)*20:pageNo*20],
					't' : t,
				}
			elif t == '2':
				results = rate[(pageNo-1)*20:pageNo*20]
				context={
					
					'results': results,
					't' : t,
				}
			elif t == '3':
				results = date[(pageNo-1)*20:pageNo*20]
				context={
					
					'results': results,
					't' : t,
				}
			elif t == '4':
				results = a_z[(pageNo-1)*20:pageNo*20]
				context={
						
					'results' : results,
					't' : t,
				}
			elif t == '5':
				results = z_a[(pageNo-1)*20:pageNo*20]
				context={
						
					'results' : results,
					't' : t,
				}
			else:
				results = pop[(pageNo-1)*20:pageNo*20]
				context={
						
					'results' : results,
					't' : t,
				}
			context['page']=pageNo
			tpages = int(len(results)/20)+1
			context['pageNumbers']=[i for i in range(1,tpages+1)]
			context['tpages']=tpages
			return render(request, 'moviegrid.html', context)
			
		else:
			name = request.GET.get('name','')
			g = request.GET.getlist('g','')
			r = request.GET.get('r','')
			ans = []
			for i in poplist:
				if name.lower() in i['title'].lower():
					ans.append(i)
			ans2 = []
			
			if g != '[]' or g != '':
				for i in ans:
					b=0
					for j in g:
						if j in i['genres']:
							b+=1
					if b == len(g):
						ans2.append(i)
			else:
				g=''
				ans2 = ans
			results = []
			if r=='6-10':
				for i in ans2:
					if i['vote_average'] > 6:
						results.append(i)
			elif r=='3-6':
				for i in ans2:
					if i['vote_average'] > 3 and i['vote_average'] < 6:
						results.append(i)
			elif r=='0-3':
				for i in ans2:
					if i['vote_average'] < 3:
						results.append(i)
			else:
				results = ans2
			context={
					'results' : results[(pageNo-1)*20:pageNo*20],
					't' : '1',
				}
			context['page']=pageNo
			context['string'] = name
			context['genress'] = g
			context['ratingss'] = r
			tpages = int(len(results)/20)+1
			context['pageNumbers']=[i for i in range(1,tpages+1)]
			context['tpages']=tpages
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
	reldate=parse(date).strftime('%B %d, %Y')
	print(reldate)
	dateyear=date[:4]

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

	movtraiurl='https://api.themoviedb.org/3/movie/'+movie_id+'/videos?api_key='+api+'&language='+lang+'&page=1'
	response0 = urllib.request.urlopen(movtraiurl)
	movtrai = json.loads(response0.read())
	movtrai=movtrai['results']
	trailers=[]
	for m in movtrai:
		if(m['type']=='Trailer'):
			trailers.append(m)

	context={
		'detail':mov,
		'date':dateyear,
		'reldate':reldate,
		'cast':cast[:15],
		'casto':cast[:7],
		'crew':crew,
		'director':director,
		'writers':writers,
		'producers':producers,
		'movsim':movsim,
		'reviews':movrev,
		'abcdef':ratingsss,
		'uvwxyz':non_ratingsss,
		'trailers':trailers[0],
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
	reldate=parse(date).strftime('%B %d, %Y')
	dateyear=date[:4]
	if(showdet['in_production']):
		enddate='current'
	else:
		enddate=showdet['last_air_date']
		enddate=enddate[:4]
	seasons=showdet['seasons']
	curr=seasons[-1]
	currairdate=parse(curr['air_date']).strftime('%B %d, %Y')
	currlastdate=parse(showdet['last_air_date']).strftime('%B %d, %Y')
	seasons=showdet['seasons']
	seasondates=[]
	for s in seasons:
		# date=parse(seasons['air_date']).strftime('%B %d, %Y')
		seasondates.append(date)

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
	keywords=[]
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
		'date': dateyear,
		'enddate': enddate,
		'curr':curr,
		'keywords':keywords,
		'reldate':reldate,
		'currairdate':currairdate,
		'currlastdate':currlastdate,
		'seasons':seasons[1:],
		'seasondates':seasondates[1:],
	}
	tv = TV.objects.get_or_create(
			name=showdet['name'],
			tv_id=show_id,
			d_rating = showdet['vote_average'],
			pic='https://image.tmdb.org/t/p/w500'+showdet['poster_path'],
			overview=showdet['overview'],
			date=reldate
		)
	return render(request, 'seriessingle.html', context)

@csrf_exempt
def search(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			query = request.POST['query']
			t = request.POST['search-type']
			# print(query,  t)
			if query:
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
				results = []
				context = {
					'results' : results,
					't' : t,
				}
				return render(request, 'search.html', context)
		else:
			return HttpResponse('Not Allowed')
	else:
		return redirect('/login/')

@csrf_exempt
def add_watchlist(request, movie_id):

	user = request.user
	m = Movie.objects.get(m_id=movie_id)
	print(m)
	watched=Watchlist.objects.filter(user=user)
	flag=0
	for watch in watched:
		if(watch.movie==m):
			flag=1
			break 
	if(flag==0):
		seens=Seenlist.objects.filter(user=user)
		flag=0
		for seen in seens:
			if(seen.movie==m):
				flag=1
				break
		if(flag==0):
			w = Watchlist.objects.create(
					user=user,
					movie=m,
				)
			w.save();
			return JsonResponse({
				'success': 'Added to Watchlist'
				})
		else:
			return JsonResponse({
				'success': 'Already in Seenlist'
				})
	else:
		return JsonResponse({
			'success' : 'Already in Watchlist'
			})

@csrf_exempt
def add_seenlist(request, movie_id):
	t = json.loads(request.body.decode('utf-8'))
	rate = t['u_rate']
	user = request.user
	m = Movie.objects.get(m_id=movie_id)
	fp = open('ratings.txt','a')
	fp.write(str(user.id)+'|'+str(m.m_id)+'|'+str(rate)+'\n')
	fp.close()
	wp=0
	seen=Seenlist.objects.filter(user=user)
	flag=0
	for s in seen:
		if(s.movie==m):
			flag=1
			break
	if(flag==0):
		watched=Watchlist.objects.filter(user=user)
		flag=0
		for watch in watched:
			if(watch.movie==m):
				flag=1
				wp = watch
				break;
		if(flag==0):
			s = Seenlist.objects.create(
					user=user,
					movie=m,
					rate=rate,
				)
			s.save();
			return JsonResponse({
					'success': 'Added to Seenlist'
					})
		else:
			s = Seenlist.objects.create(
					user=user,
					movie=m,
					rate=rate,
				)
			s.save()
			Watchlist.objects.get(id=wp.id).delete()
			return JsonResponse({
				'success': 'Added to Seenlist'
				})
	else:
		return JsonResponse({
				'success': 'Already in Seenlist'
			})

def seen(request):
	seens=Seenlist.objects.filter(user=request.user).order_by('-time_added')
	context={
		'seenMovies':seens,
	}
	return render(request, 'seenlist.html', context)

def watch(request):
	watch=Watchlist.objects.filter(user=request.user).order_by('-time_added')
	rate = Watchlist.objects.filter(user=request.user).order_by('-movie__d_rating')
	if request.method == 'POST':
		t = request.POST['filter']
		context={
			't': t,
		}
		if t == '1':
			context['watchMovies'] = watch
		else:
			context['watchMovies'] = rate
		return render(request, 'watchlist.html', context)
	else:
		context = {
			'watchMovies':watch
		}
		return render(request, 'watchlist.html', context)

def profile(request):
	pro=Profile.objects.get(user=request.user)
	user=User.objects.get(id=request.user.id)
	msg = ''
	watch=Watchlist.objects.filter(user=request.user)
	seen=Seenlist.objects.filter(user=request.user)
	watch=len(watch)
	seen=len(seen)
	if request.method == 'POST':
		if 'change_pic' in request.POST:
			if request.FILES:
					myfile = request.FILES['myfile']
					fs = FileSystemStorage()
					filename = fs.save(myfile.name, myfile)
					pro.profilePic=filename
			pro.save()
			msg = 'Successfully Updated Profile Picture'
	context={
		'profile': pro,
		'msg' : msg,
		'seen':seen,
		'watch':watch,
	}
	return render(request, 'profile.html', context)		

@csrf_exempt
def add_watchlist2(request, tv_id):
	user = request.user
	m = TV.objects.get(tv_id=tv_id)
	watched=WatchlistTV.objects.filter(user=user)
	flag=0
	for watch in watched:
		if(watch.tv==m):
			flag=1
			break 
	if(flag==0):
		seens=SeenlistTV.objects.filter(user=user)
		flag=0
		for seen in seens:
			if(seen.tv==m):
				flag=1
				break
		if(flag==0):
			w = WatchlistTV.objects.create(
					user=user,
					tv=m,
				)
			w.save();
			return JsonResponse({
				'success': 'Added to Watchlist'
				})
		else:
			return JsonResponse({
				'success': 'Already in Seenlist'
				})
	else:
		return JsonResponse({
			'success' : 'Already in Watchlist'
			})

@csrf_exempt
def add_seenlist2(request, tv_id):
	t = json.loads(request.body.decode('utf-8'))
	rate = t['u_rate']
	user = request.user
	m = TV.objects.get(tv_id=tv_id)
	fp = open('ratings2.txt','a')
	fp.write(str(user.id)+'|'+str(m.tv_id)+'|'+str(rate)+'\n')
	fp.close()
	wp=0
	seen=SeenlistTV.objects.filter(user=user)
	flag=0
	for s in seen:
		if(s.tv==m):
			flag=1
			break
	if(flag==0):
		watched=WatchlistTV.objects.filter(user=user)
		flag=0
		for watch in watched:
			if(watch.tv==m):
				flag=1
				wp = watch
				break;
		if(flag==0):
			s = SeenlistTV.objects.create(
					user=user,
					tv=m,
					rate=rate,
				)
			s.save();
			return JsonResponse({
					'success': 'Added to Seenlist'
					})
		else:
			s = SeenlistTV.objects.create(
					user=user,
					tv=m,
					rate=rate,
				)
			s.save()
			WatchlistTV.objects.get(id=wp.id).delete()
			return JsonResponse({
				'success': 'Added to Seenlist'
				})
	else:
		return JsonResponse({
				'success': 'Already in Seenlist'
			})

def seen2(request):
	seens=SeenlistTV.objects.filter(user=request.user).order_by('-time_added')
	context={
		'seenTV':seens,
	}
	return render(request, 'seenlist2.html', context)

def watch2(request):
	watch=WatchlistTV.objects.filter(user=request.user).order_by('-time_added')
	rate = WatchlistTV.objects.filter(user=request.user).order_by('-tv__d_rating')
	if request.method == 'POST':
		t = request.POST['filter']
		context={
			't': t,
		}
		if t == '1':
			context['watchTV'] = watch
		else:
			context['watchTV'] = rate
		return render(request, 'watchlist2.html', context)
	else:
		context = {
			'watchTV':watch
		}
		return render(request, 'watchlist2.html', context)


def changepass(request):
	msg=''
	user=User.objects.get(id=request.user.id)
	pro=Profile.objects.get(user=user)
	if request.method=='POST':
		p1 = request.POST['pass1']
		p2 = request.POST['pass2']
		if p1 == p2:
			user.set_password(p1)
			user.save()
			logout(request)
			msg="Successfully Changted Password"
			return redirect('/login/')
		else:
			msg='Passwords Do No Match'
	context={
		'msg' : msg,
		'profile':pro,
	}
	return render(request, 'changepass.html', context)
