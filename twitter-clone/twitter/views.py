from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            mail = request.POST['email']
            pwd = request.POST['password']
            user = authenticate(request, username=mail, password=pwd)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid credentials')
                return render(request, 'login.html') 
        elif 'cancel' in request.POST:
            return redirect('index')
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        if 'register' in request.POST:
            return HttpResponse('register')
        elif 'cancel' in request.POST:
            return redirect('index')
    else:
        return render(request, 'register.html')

def home(request):
    return render(request, 'home.html')