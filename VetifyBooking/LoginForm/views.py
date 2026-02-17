from django.shortcuts import render
from django.http import HttpResponse

def login_view(request):
    return render(request, 'LoginForm/login.html')

def register_view(request):
    return render(request, 'LoginForm/register.html')
#hola
