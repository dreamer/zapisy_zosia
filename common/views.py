from django.shortcuts import render_to_response, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import *

from django.contrib.auth.models import User

def login_view(request):
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(username=email, password=password)
    if user is not None:
        if user.is_active:
            login(request,user)
        else:
            print 'disabled account'
    else:
        print 'invalid login'
    return HttpResponseRedirect('/blog/')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/blog/')

