__author__ = 'Tadej'
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login, logout


def login(request):
     return render(request, 'app/login.html')

def login_action(request):
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            django_login(request, user)
            return redirect('/app/index')
        else:
            print('not active')
    else:
        print('nok')
        return redirect('/app/login')

def logout_view(request):
    logout(request)
    return redirect('/app/login')