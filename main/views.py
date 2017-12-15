# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def index(request):
	return render(request, 'index.html')

def base(request):
	return render(request, 'base.html')

def list(request):
	return render(request, 'moviegrid.html')

