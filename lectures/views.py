# -*- coding: UTF-8 -*-

from django.http import *
from django.template import Context
from django.template.loader import get_template
from django.shortcuts import render_to_response

from django.contrib.auth.decorators import login_required
from datetime import datetime
from common.forms import LoginForm

from models import *
from forms import *

def index(request):
    title = "Lectures"
    user = request.user
    login_form = LoginForm()
    lectures = Lecture.objects.filter(accepted=True)
    if user.is_authenticated():
        lecture_proposition_form = NewLectureForm()
        if request.method == 'POST':
            lecture_proposition_form = NewLectureForm(request.POST)
            if lecture_proposition_form.is_valid():
                form = lecture_proposition_form
                l = Lecture( title     = form.cleaned_data['title'],
                             duration  = form.cleaned_data['duration'],
                             abstract  = form.cleaned_data['abstract'],
                             #info      = form.cleaned_data['info'],
                             date_time = datetime.now(),
                             author    = "foobar", #user.last_name + " " + user.first_name,
                             accepted  = False
                           )
                l.save()
                messages = [ "Thank you! Your lecture suggestion has been sent and is awaiting moderation." ]
    return render_to_response('lectures.html', locals())

