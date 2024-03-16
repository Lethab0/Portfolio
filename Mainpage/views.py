from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    return render(request , 'Mainpage/index.html')

