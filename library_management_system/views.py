from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
def home(request):
    return render(request, 'home.html')

def index(request):
    return HttpResponse("Welcome to the Library Management System.")

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error', 'Invalid credentials'})
        return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            return render(request, 'signup.html', {'error': 'Password do not match'})

        try:
            user.objects.create_user(username=username, password=password1)
            return redirect('login')
        except:
            return render(request, 'signup.html', {'error': 'Username already exists'})
    

    return render(request, 'signup.html')

