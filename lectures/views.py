# -*- coding: UTF-8 -*-

from django.http import *
from django.template import Context
from django.template.loader import get_template
from django.shortcuts import render_to_response

from django.contrib.auth.decorators import login_required
from common.forms import LoginForm

from models import *
from forms import *

def index(request):
    title = "Lectures"
    user = request.user
    login_form = LoginForm()
    lectures = Lecture.objects.filter(accepted=True)
    if user.is_authenticated() and user.is_active:
        lecture_proposition_form = NewLectureForm()
        if request.method == 'POST':
            lecture_proposition_form = NewLectureForm(request.POST)
            if lecture_proposition_form.is_valid():
                form = lecture_proposition_form
                Lecture.objects.create_lecture(form, request.user)
                messages = [ "Thank you! Your lecture suggestion has been sent and is awaiting moderation." ]
    return render_to_response('lectures.html', locals())

