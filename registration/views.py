# -*- coding: UTF-8 -*-

from django.shortcuts import render_to_response, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from forms import RegisterForm
from models import UserPreferences

from common.forms import LoginForm

def suggested_username( name, surname ):
    # deprecated, probably not needed
    # TODO: make database query if username is not already in base
    return '%s_%s' % ( name, surname )

def register(request):
    user = request.user
    title = "Registration"
    # login_form = LoginForm()

    #if user.is_authenticated:
    #    return HttpResponseRedirect('/blog/')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email    = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = suggested_username( form.cleaned_data['name'],
                                           form.cleaned_data['surname'])
            try:
                user = User.objects.get(email=email)
                return HttpResponseRedirect('/register/recover/')
            except User.DoesNotExist:
                #user = User(username=email, password=password, email=email)
                user = User.objects.create_user(email, email, password)
                user.first_name = form.cleaned_data['name']
                user.last_name  = form.cleaned_data['surname']
                user.save()
            prefs = UserPreferences(user=user)
            prefs.day_1       = form.cleaned_data['day_1']
            prefs.day_2       = form.cleaned_data['day_2']
            prefs.day_3       = form.cleaned_data['day_3']
            prefs.breakfast_2 = form.cleaned_data['breakfast_2']
            prefs.breakfast_3 = form.cleaned_data['breakfast_3']
            prefs.breakfast_4 = form.cleaned_data['breakfast_4']
            prefs.dinner_1    = form.cleaned_data['dinner_1']
            prefs.dinner_2    = form.cleaned_data['dinner_2']
            prefs.dinner_3    = form.cleaned_data['dinner_3']
            prefs.bus         = form.cleaned_data['bus']
            prefs.vegetarian  = form.cleaned_data['vegetarian']
            prefs.save()
            return HttpResponseRedirect('/register/thanks/')
    else:
        form = RegisterForm()
    return render_to_response('register_form.html', locals())


def thanks(request):
    user = request.user
    title = "Registration"
    login_form = LoginForm()
    return render_to_response('thanks.html', locals())
    
# TODO
#def add_organization(request):
#    HttpResponse('foo',mimetype="application/xhtml+xml")

def recover(request):
    user = request.user
    title = "Password recovery"
    login_form = LoginForm()

    return render_to_response('recover.html', locals())

