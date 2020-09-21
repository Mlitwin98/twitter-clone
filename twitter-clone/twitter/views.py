from django.shortcuts import render
from django.http.response import HttpResponse

# Create your views here.
def main(request):
    return render(request, 'index.html')

def login(request):
    return HttpResponse('Login')

def register(request):
    return HttpResponse('Register')