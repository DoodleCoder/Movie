# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from main.models import *
from django.contrib import admin

# Register your models here.

admin.site.register(Profile)
admin.site.register(Movie)
admin.site.register(TV)
admin.site.register(Watchlist)
admin.site.register(WatchlistTV)
admin.site.register(SeenlistTV)
admin.site.register(Seenlist)
admin.site.register(Genre)