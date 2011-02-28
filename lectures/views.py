# -*- coding: UTF-8 -*-

from django.utils.translation import ugettext as _
from django.http import *
from django.template import Context
from django.template.loader import get_template
from django.shortcuts import render_to_response

from django.contrib.auth.decorators import login_required
from common.forms import LoginForm
from common.helpers import *

from models import *
from forms import *

def index(request):
    title = "Lectures"
    user = request.user
    lectures = Lecture.objects.filter(accepted=True)
    if is_lecture_suggesting_enabled():
        login_form = LoginForm()
        if user.is_authenticated() and user.is_active:
            if request.method == 'POST':
                lecture_proposition_form = NewLectureForm(request.POST)
                if lecture_proposition_form.is_valid():
                    form = lecture_proposition_form
                    Lecture.objects.create_lecture(form, request.user)
                    messages = [ _("thankyou") ]
                    lecture_proposition_form = NewLectureForm()
            else:
                lecture_proposition_form = NewLectureForm()
    return render_to_response('lectures.html', locals())


def program(request):
    title = "Program"
    user = request.user
    return render_to_response('program.html', locals())

