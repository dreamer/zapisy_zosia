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
from django.views.decorators.cache import never_cache
from common.helpers import *


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
    return HttpResponseRedirect('/login/?next=/change_preferences/') # yeah, right...


def register(request):
    if is_registration_disabled():
        raise Http404

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
            username = form.cleaned_data['email']
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


def regulations(request):
    # Setting title makes "Registration" link visible on the panel.
    title = "Registration" 
    return render_to_response('regulations.html', locals())

def thanks(request):
    user = request.user
    title = "Registration"
    login_form = LoginForm()
    return render_to_response('thanks.html', locals())
 
def count_payment(user):
    # hmm, we want to work for preferences, too
    if user.__class__ == UserPreferences:
        prefs = user
    else:
        prefs = UserPreferences.objects.get(user=user)

    # returns how much money user is going to pay
    # ok, temporarily it is hardcoded, probably should
    # be moved somewhere else
    days_payment        = (prefs.day_1       + prefs.day_2       + prefs.day_3)       * 40
    breakfasts_payment  = (prefs.breakfast_2 + prefs.breakfast_3 + prefs.breakfast_4) * 15 
    dinners_payment     = (prefs.dinner_1    + prefs.dinner_2    + prefs.dinner_3)    * 20
    transport_payment   = 0;
    if prefs.bus: transport_payment += 45;
    bonus_payment       = 15
    if prefs.day_1 and prefs.breakfast_2 and prefs.dinner_1: bonus_payment -= 10
    if prefs.day_2 and prefs.breakfast_3 and prefs.dinner_2: bonus_payment -= 10
    if prefs.day_3 and prefs.breakfast_4 and prefs.dinner_3: bonus_payment -= 10
    return days_payment + breakfasts_payment + dinners_payment + bonus_payment + transport_payment

@never_cache
@login_required
def change_preferences(request):
    user = request.user
    title = "Change preferences"
    prefs = UserPreferences.objects.get(user=user)
    form = ChangePrefsForm()
    user_paid = prefs.paid
    if request.POST:
        # raise Http404 # the most nooby way of blocking evar (dreamer_)
        form = ChangePrefsForm(request.POST)
        # bug with settings not updateble
        # after user paid
        if user_paid: # remove or True after zosia
            post = request.POST
            rewritten_post = {}
            for k in post.keys():
                rewritten_post[k] = post[k]
            for k in [ 'day_1', 'day_2', 'day_3',
                       'breakfast_2', 'breakfast_3', 'breakfast_4',
                       'dinner_1', 'dinner_3', 'dinner_2' ]:
                if prefs.__dict__[k]:
                    rewritten_post[k] = u'on'
            rewritten_post['shirt_type'] = prefs.__dict__['shirt_type']
            rewritten_post['shirt_size'] = prefs.__dict__['shirt_size']
            form = ChangePrefsForm(rewritten_post)
        form.add_bad_org(prefs)
        form.set_paid(user_paid)
        if form.is_valid():
            # save everything
            prefs.org = Organization.objects.get(id=form.cleaned_data['organization_1'])
            if prefs.paid:
                pass
            else:
                prefs.day_1       = form.cleaned_data['day_1']
                prefs.day_2       = form.cleaned_data['day_2']
                prefs.day_3       = form.cleaned_data['day_3']
                prefs.breakfast_2 = form.cleaned_data['breakfast_2']
                prefs.breakfast_3 = form.cleaned_data['breakfast_3']
                prefs.breakfast_4 = form.cleaned_data['breakfast_4']
                prefs.dinner_1    = form.cleaned_data['dinner_1']
                prefs.dinner_2    = form.cleaned_data['dinner_2']
                prefs.dinner_3    = form.cleaned_data['dinner_3']
                prefs.shirt_size  = form.cleaned_data['shirt_size']
                prefs.shirt_type  = form.cleaned_data['shirt_type']
            prefs.bus         = form.cleaned_data['bus']
            prefs.vegetarian  = form.cleaned_data['vegetarian']
            prefs.save()
            payment = count_payment(user)

    else:
        form.initialize(prefs)
        payment = count_payment(user)
    user_wants_bus = prefs.bus
    return render_to_response('change_preferences.html', locals())

@login_required
def users_status(request):
    if not ( request.user.is_staff and request.user.is_active ):
        raise Http404
    # nie no, to jest źle...
    # users = User.objects.all()
    # prefs = UserPreferences.objects.all()
    #list = zip(users,prefs)
    list = []
    return render_to_response('the_great_table.html', locals())

def register_payment(request):
    user = request.user
    if not user.is_authenticated() or not user.is_staff or not user.is_active:
        raise Http404
    if not request.POST:
        raise Http404
    pid = request.POST['id']
    prefs = UserPreferences.objects.get(id=pid)
    prefs.paid = True
    prefs.save()
    return HttpResponse("ok")

# TODO(Karol): remove after successful verification.
"""
def register_bus_payment(request):
    user = request.user
    if not user.is_authenticated() or not user.is_staff or not user.is_active:
        raise Http404
    if not request.POST:
        raise Http404
    pid = request.POST['id']
    prefs = UserPreferences.objects.get(id=pid)
    prefs.paid_for_bus = True
    prefs.save()
    return HttpResponse("ok")
"""
