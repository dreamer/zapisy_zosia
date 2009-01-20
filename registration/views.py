# -*- coding: UTF-8 -*-

from django.shortcuts import render_to_response, HttpResponse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from django.contrib.auth import logout
from forms import *
from models import UserPreferences, Organization
from common.forms import LoginForm
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.http import base36_to_int, int_to_base36
from django.template import Context, loader
from django.contrib.sites.models import RequestSite
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required


def activate_user(request, uidb36=None, token=None):
    assert uidb36 is not None and token is not None
    try:
        uid_int = base36_to_int(uidb36)
        usr = get_object_or_404(User, id=uid_int)
    except Exception:
        return render_to_response('reactivation.html', {})
    if token_generator.check_token(usr, token):
        usr.is_active = True
        usr.save()
    else:
        return render_to_response('reactivation.html', {})
    return HttpResponseRedirect('/login/') # yeah, right...


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
                return HttpResponseRedirect('/password_reset/')
            except User.DoesNotExist:
                user = User.objects.create_user(email, email, password)
                user.first_name = form.cleaned_data['name']
                user.last_name  = form.cleaned_data['surname']
                user.is_active = False
                # send activation mail
                t = loader.get_template("activation_email.txt")
                c = {
                    'site_name': RequestSite(request),
                    'uid': int_to_base36(user.id),
                    'token': token_generator.make_token(user),
                }
                send_mail( _('activation_mail_title'), 
                            t.render(Context(c)),
                           'from@example.com',
                            [ user.email ], 
                            fail_silently=True )
                user.save()
            #saving organization
            try:
                org1 = form.cleaned_data['organization_1']
                org2 = form.cleaned_data['organization_2']
                if org1 == 'new':
                    org = Organization(name=org2, accepted=False)
                    org.save()
                else:
                    org = Organization.objects.get(id=org1)
            except Exception:
                org = Organization("fail",accepted=False)
                org.save()
            prefs = UserPreferences(user=user)
            prefs.org         = org
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
            prefs.shirt_size  = form.cleaned_data['shirt_size']
            prefs.shirt_type  = form.cleaned_data['shirt_type']
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
 
def count_payment(user):
    # returns how much money user is going to pay
    # ok, temporarily it is hardcoded, probably should
    # be moved somewhere else
    prefs = UserPreferences.objects.get(user=user)
    days_payment        = (prefs.day_1       + prefs.day_2       + prefs.day_3)       * 50
    breakfasts_payment  = (prefs.breakfast_2 + prefs.breakfast_3 + prefs.breakfast_4) * 8
    dinners_payment     = (prefs.dinner_1    + prefs.dinner_2    + prefs.dinner_3)    * 10
    bonus_payment       = 0
    if prefs.day_1 and prefs.breakfast_2 and prefs.dinner_1: bonus_payment -= 1
    if prefs.day_2 and prefs.breakfast_3 and prefs.dinner_2: bonus_payment -= 1
    if prefs.day_3 and prefs.breakfast_4 and prefs.dinner_3: bonus_payment -= 1
    return days_payment + breakfasts_payment + dinners_payment + bonus_payment


@login_required
def change_preferences(request):
    user = request.user
    title = "Change preferences"
    prefs = UserPreferences.objects.get(user=user)
    form = ChangePrefsForm()
    if request.POST:
        form = ChangePrefsForm(request.POST)
        form.add_bad_org(prefs)
        if form.is_valid():
            # save everything
            prefs.org         = Organization.objects.get(
                                    id=form.cleaned_data['organization_1'])
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
            prefs.shirt_size  = form.cleaned_data['shirt_size']
            prefs.shirt_type  = form.cleaned_data['shirt_type']
            prefs.save()
    else:
        form.initialize(prefs)
    payment = count_payment(user)
    return render_to_response('change_preferences.html', locals())

