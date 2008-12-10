# -*- coding: UTF-8 -*-

from django.http import *
from django.template import Context
from django.template.loader import get_template
from django.shortcuts import render_to_response

from django.contrib.auth.decorators import login_required
from datetime import datetime
#from forms import *

from models import *

def index(request):
    title = "Lectures"
    user = request.user
    lectures = Lecture.objects.filter(accepted=True)
    """
    n = len(lectures)
    if request.user.is_authenticated():
        form = LectureForm()
        if request.method == 'POST':
            form = LectureForm(request.POST)
            if form.is_valid():
                # dodaj do bazy
                # wyciąganie danych z POST w ten sposób gwarantuje poprawnosc typów
                l = Lecture( title = form.clean_data['title'],
                             duration  = form.clean_data['duration'],
                             abstract  = form.clean_data['abstract'],
                             info      = form.clean_data['info'],
                             date_time = datetime.now(),
                             author    = user.last_name + " " + user.first_name,
                             accepted  = False
                           )
                l.save()
                messages = [ "Thank you! Your lecture is awaiting moderation." ]
                return render_to_response('lectures.html', locals())
    """
    return render_to_response('lectures.html', locals())

