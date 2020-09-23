from django.shortcuts import render, redirect
from django.http.response import HttpResponse

# Create your views here.
def main(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            return HttpResponse('login')
        elif 'cancel' in request.POST:
            return redirect('main')
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        if 'register' in request.POST:
            return HttpResponse('register')
        elif 'cancel' in request.POST:
            return redirect('main')
    else:
        return render(request, 'register.html')