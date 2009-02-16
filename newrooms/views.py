# -*- coding: UTF-8 -*-

from django.http import *
from django.template import Context
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
import random
from models import *
from datetime import *

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
                      short_unlock_time = datetime.now()
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
    # get correct room based on rid
    room_number = request.POST['rid'][1:]
    room = NRoom.objects.get(number=room_number)
    status = room.get_status()
    json = ''
    if status == 0: # for debug purposes
        # case when room is empty
        timeout = timedelta(0,120,0) # 2 minutes
        room.short_unlock_time = datetime.now() + timeout
        room.save()
        json = '{"msg":"you locked"}'
        # case when room is not empty
        # ...
    elif status == 1: # room is locked
        # case when its long lock
        # ...
        # case when its short lock
        json = '{"msg":"short_lock"}'

    return HttpResponse(json, mimetype="application/json")

