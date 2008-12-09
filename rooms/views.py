# -*- coding: UTF-8 -*-

from django.http import *
from django.template import Context
from django.template.loader import get_template
from django.shortcuts import render_to_response

from models import *

def index(request):
    user = request.user
    rooms_list = Room.objects.all()
    return render_to_response('rooms.html',locals())

