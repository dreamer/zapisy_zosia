# -*- coding: UTF-8 -*-

from django.shortcuts import render_to_response, HttpResponse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from django.contrib.auth import logout
from forms import RegisterForm
from models import UserPreferences
from common.forms import LoginForm
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.http import base36_to_int, int_to_base36
from django.template import Context, loader
from django.contrib.sites.models import RequestSite


def suggested_username( name, surname ):
    # deprecated, probably not needed
    # TODO: make database query if username is not already in base
    return '%s_%s' % ( name, surname )

def activate_user(request, uidb36=None, token=None):
    assert uidb36 is not None and token is not None
    try:
        uid_int = base36_to_int(uidb36)
    except ValueError:
        raise Http404
    usr = get_object_or_404(User, id=uid_int)
    if token_generator.check_token(usr, token):
        usr.is_active = True
        usr.save()
    else:
        raise Http404
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
    
# TODO
#def add_organization(request):
#    HttpResponse('foo',mimetype="application/xhtml+xml")

