"""grmovies URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from main import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^index/', views.index),
    url(r'^base/$', views.base),
    url(r'^search/$', views.search),
    url(r'^movielist/(?P<page_no>\d+)/$', views.movielist),
    url(r'^tvlist/(?P<page_no>\d+)/$', views.tvlist),
    url(r'^login/$', views.login_site),
    url(r'^add_watchlist/(?P<movie_id>\d+)/$', views.add_watchlist),
    url(r'^add_watchlist2/(?P<tv_id>\d+)/$', views.add_watchlist2),
    url(r'^add_seenlist2/(?P<tv_id>\d+)/$', views.add_seenlist2),
    url(r'^add_seenlist/(?P<movie_id>\d+)/$', views.add_seenlist),
    url(r'^register/$', views.register),
    url(r'^logout/$', views.logout_site),
    url(r'^movie/(?P<movie_id>\d+)/$', views.movie),
    url(r'^show/(?P<show_id>\d+)/$', views.show),
    url(r'^movieseenlist/$', views.seen),
    url(r'^moviewatchlist/$', views.watch),
    url(r'^tvseenlist/$', views.seen2),
    url(r'^tvwatchlist/$', views.watch2),
    url(r'^profile/$', views.profile),



]
