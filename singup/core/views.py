from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def index(request):
    return render(request, 'authentication/index.html')


def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if User.objects.filter(username=username):
            messages.error(request, 'Username already exist!')
            return redirect('signup')

        if User.objects.filter(email=email):
            messages.error(request, 'Email already exist')
            return redirect('signup')
        
        if password1 == password2:
            myuser = User.objects.create_user(username, email, password1)

            myuser.save()

            messages.success(request, 'Your account has been successfully created.')

            return redirect('signin')

        else:
            messages.error(request, 'Passwords do not match')

    return render(request, 'authentication/signup.html')  


def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']


        user = authenticate(username=username, password=password1)

        if user is not None:
            login(request, user) 
            fname = user.username
            return render(request, 'authentication/index.html', {'fname': fname})
        else: 
            messages.error(request, 'Bad credentials')
            return redirect('index')

    return render(request, 'authentication/signin.html')


def signout(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('index')
