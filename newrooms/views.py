# -*- coding: UTF-8 -*-

from django.http import *
from django.template import Context
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
import random
from models import *

# from models import *

@login_required
def index(request):
    user = request.user
    title = "Rooms"
    #rooms_list = Room.objects.all()
    return render_to_response('rooms.html',locals())


def fill_rooms(request):
    # maybe update this for serious usage?
    def save_room(n,c):
        room = NRoom( number = "%s"%n,
                      capacity = c,
                      password = "",
                    )
        room.save()
    for n in range(102,115): save_room(n,6)
    for n in range(202,215): save_room(n,4)
    for n in range(302,315): save_room(n,2)
    save_room(301,4)
    return HttpResponse("ok")


@login_required
def json_rooms_list(request):
    json = NRoom.objects.to_json()
    return HttpResponse(json, mimetype="application/json")


@login_required
def modify_room(request):
    if not request.POST: raise Http404

    room_number = request.POST['rid'][1:]
    r = NRoom.objects.get(number=room_number)
    if r.password == '':
        r.password = 'xx'
    else:
        r.password = ''
    r.save()
    return HttpResponse("ok")
    #return HttpResponse("ok", mimetype="application/json")

