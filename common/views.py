from django.shortcuts import render_to_response, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, PasswordChangeForm
from forms import *

def login_view(request):
    title = "Login"
    user = request.user
    if not user.is_authenticated():
        form = LoginForm()
        try:
            reason = None # theistic code ;)
            greetings_stranger = False
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
        if not reason and not greetings_stranger:
            # login quietly
            referer = request.META['HTTP_REFERER']
            if referer.endswith('/login/') or referer.endswith('/bye/'):
                referer = '/blog/'
            return HttpResponseRedirect(referer)
    # this template acutally is used only in case of unsuccesfull login
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

