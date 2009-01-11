from django.shortcuts import render_to_response, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, PasswordChangeForm
from forms import *

def login_view(request):
    # hmm, I've moved too much stuff in here, it's a bit messy
    # and HTTP_REFERER trickery should probably be better handled
    # but it's 6 a.m. already
    # Special thanks to my good friend, caffeine (dreamer_)
    title = "Login"
    user = request.user
    try:
        referer = request.META['HTTP_REFERER']
    except Exception:
        referer = ''
    if not user.is_authenticated():
        form = LoginForm()
        try:
            reason = None # theistic code ;)
            greetings_stranger = False
            greetings_resetter = False
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(username=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                else:
                    reason = 'LOGIN_account_disabled'
            else:
                reason = 'LOGIN_invalid'
        except Exception:
            greetings_stranger = True
        if referer.endswith('/reset/done/'):
            greetings_resetter = True
            greetings_stranger = False
        if not reason and not greetings_stranger and not greetings_resetter:
            # login quietly
            if referer.endswith('/login/') or referer.endswith('/bye/') or referer.endswith('/reset/done/'):
                referer = '/blog/'
            return HttpResponseRedirect(referer)
    # this template is used in case of:
    # - unsuccesfull login
    # - login after password reset (aka 'password recovery')
    return render_to_response('login.html', locals())

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/logout/bye/')

def thanks(request):
    user = request.user
    title = "Bye!"
    login_form = LoginForm()
    return render_to_response('bye.html', locals())


@login_required
def password_change(request):
    user = request.user
    title = "Change password"
    if request.method == "POST":
        pc_form = PasswordChangeForm(request.user, request.POST)
        if pc_form.is_valid():
            pc_form.save()
            return HttpResponseRedirect("done/")
    else:
        pc_form = PasswordChangeForm(request.user)
    return render_to_response("change_password.html", locals())

@login_required
def password_change_done(request):
    user = request.user
    title = "Change password"
    return render_to_response("change_password_done.html", locals())

