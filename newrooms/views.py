# -*- coding: UTF-8 -*-

from django.views.decorators.cache import cache_page
from django.http import *
from django.template import Context
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from registration.models import UserPreferences
import random
from models import *
from datetime import *
from common.helpers import *

# from models import *

@login_required
def index(request):
	user = request.user
	title = "Rooms"
	if has_user_opened_records(user):
 	   return render_to_response('rooms.html',locals())
	else:
                prefs = UserPreferences.objects.get(user=user)
                user_openning_hour = datetime(2011,2,26,20,00) - timedelta(minutes=prefs.minutes_early)                
		return render_to_response('rooming_disabled.html',locals())


def fill_rooms(request):
    # maybe update this for serious usage?
    def save_room(n,b,c):
        room = NRoom( number = "%s %s"%(b,n),
                      capacity = c,
                      password = "",
                      short_unlock_time = datetime.now()
                    )
        room.save()

    for n in [1,2,3]:
        save_room(n,'A',4)
    save_room(101,'A',3)
    save_room(102,'A',4)
    save_room(103,'A',4)
    save_room(104,'A',2)
    save_room(105,'A',4)
    save_room(106,'A',4)
    save_room(107,'A',3)
    save_room(108,'A',2)
    save_room(109,'A',2)
    save_room('półpiętro','A',1)
    save_room(201,'A',2)
    save_room(202,'A',2)
    save_room(203,'A',3)
    save_room(204,'A',3)
    save_room(205,'A',2)
    save_room(206,'A',4)
    save_room(208,'A',3)
    save_room('apartament','A',6)

    save_room(1,'B',3)
    save_room(2,'B',2)
    save_room(3,'B',2)
    save_room(4,'B',2)
    save_room(5,'B',2)
    save_room(6,'B',2)
    save_room(7,'B',2)
    save_room(8,'B',2)
    save_room(9,'B',2)
    save_room(10,'B',4)
    save_room(11,'B',2)
    save_room(12,'B',1)
    save_room(101,'B',4)
    save_room(102,'B',2)
    save_room(103,'B',2)
    save_room(104,'B',2)
    save_room(105,'B',2)
    save_room(106,'B',2)
    save_room(107,'B',4)
    save_room(108,'B',4)
    save_room(109,'B',2)
    save_room(110,'B',4)
    save_room(111,'B',2)
    save_room(112,'B',1)
    save_room(201,'B',4)
    save_room(202,'B',2)
    save_room(203,'B',3)
    save_room(204,'B',2)
    save_room(205,'B',2)
    save_room(206,'B',2)
    save_room(207,'B',2)
    save_room(208,'B',2)
    save_room(209,'B',2)
    save_room(210,'B',2)
    save_room(211,'B',4)

    return HttpResponse("ok")


#@login_required
@cache_page(30)
def json_rooms_list(request):
    json = NRoom.objects.to_json()
    return HttpResponse(json, mimetype="application/json")

def dict_to_json(d):
    ret = []
    for k,v in d.items(): ret.append('"%s":"%s"'%(k,v))
    return '{%s}'%(','.join(ret))


def get_in_room(usr,room,own=False):
    occupation = UserInRoom( locator=usr,
                             room=room,
                             ownership=own
                           )
    occupation.save()

def get_room_locators(room):
    # return html
    occs = UserInRoom.objects.filter(room=room)
    if not occs:
        return ''
    else:
        lst =  ','.join( [ u" %s"%o.locator for o in occs ] )
        return u"Mieszkają tu: %s<br/>" % lst

@login_required
def trytogetin_room(request):
    if not request.POST: raise Http404
    if not has_user_opened_records(request.user): return HttpResponse('fail')
    room = NRoom.objects.get(id=int(request.POST['rid']))
    if room.password == request.POST['key']:
        get_in_room(request.user, room)
        return HttpResponse('ok')
    return HttpResponse('fail')

@login_required
def open_room(request):
    if not request.POST: raise Http404
    if not has_user_opened_records(request.user): return HttpResponse('fail')
    occupation = UserInRoom.objects.get(locator=request.user)
    if occupation.ownership:
        room = occupation.room
        if room.password == request.POST['key']:
            occupation.room.short_unlock_time = datetime.now()
            occupation.room.save()
            return HttpResponse('ok')

@login_required
def close_room(request):
    if not request.POST: raise Http404
    if not has_user_opened_records(request.user): return HttpResponse('fail')
    occupation = UserInRoom.objects.get(locator=request.user)
    if occupation.ownership:
        room = occupation.room
        if room.password == request.POST['key']:
    	    no_locators = UserInRoom.objects.filter(room=room).count()
	    if no_locators == 1: # user is still alone in this room
                timeout = timedelta(0,10800,0) # 3h == 10800s
                occupation.room.short_unlock_time = datetime.now() + timeout
                occupation.room.save()
                return HttpResponse('ok')


CONST_LEAVE_ROOM_BTN = u'<button onclick=\'window.location=/leave_room/\'>Opuść pokój</button>'
CONST_OK_BTN = u'<button onclick=\'hideDialog()\'>OK</button>'
CONST_OK2_BTN = u'<button onclick=\'hideDialog()\'>Zostań w pokoju</button>'
# CONST_LEAVE_OPEN_ROOM_BTN = u'<button onclick=\'Rooms.hideDialog(1)\'>Otwórz pokój</button>'
# CONST_USE_KEY_BTN = u'<button>Zamknij pokój</button>'
def leave_open_room_btn(key): return u'<button onclick=\'Rooms.hideDialog(%s)\'>Wejdź i nie zamykaj</button>' % key
def close_room_btn(key): return u'<button onclick=\'Rooms.closeRoom(%s)\'>Wejdź i zamknij kluczem</button>' % key
CONST_FORM = u"""<form><input type=\'submit\' value=\'Ustaw hasło\'/></form>"""


@login_required
def leave_room(request):
    try:
        prev_occupation = UserInRoom.objects.get(locator=request.user)
        prev_occupation.delete()
    except Exception: pass
    # finally: TODO check which versions of Python support 'finally' keyword
    return HttpResponseRedirect('/rooms/')


@login_required
def modify_room(request):
    if not request.POST: raise Http404
    # get correct room based on rid
    room_number = request.POST['rid'][1:]
    room = NRoom.objects.get(number=room_number)
    status = room.get_status()
    json = { "room_number":room_number, "buttons":'', 'msg':'', 'form':'' }
    prev_occupation = None
    try:
        prev_occupation = UserInRoom.objects.get(locator=request.user)
    except Exception:
        pass
    if status == 0:
        #
        # this room is open
        #
        msg = ''
        no_locators = room.get_no_locators()
        if no_locators == 0:
            #
            # case when room is empty
            #
            if prev_occupation:
                json['msg'] = u"<br/>Jeśli chcesz się dopisać do tego pokoju,<br/>musisz najpierw wypisać się z pokoju %s.<br/>" % prev_occupation.room
                json['buttons'] = CONST_OK_BTN
            else:
                get_in_room(request.user, room, True)
                timeout = timedelta(0,120,0) # 2 minutes
                room.short_unlock_time = datetime.now() + timeout
                room.password = ''.join([ str(random.choice(range(10))) for _ in range(6) ])
                room.save()
                json['msg'] = u"<br/>Przekaż klucz swoim znajomym, aby<br/>mogli dołączyć do tego pokoju.<br/><br/>"
                json['form'] = u"Klucz do pokoju: <strong>%s</strong><br/>" % room.password
                json['buttons'] = close_room_btn(room.password) + leave_open_room_btn(room.password) + CONST_LEAVE_ROOM_BTN
        else:
            #
            # case when room is not empty
            #
            if (prev_occupation is not None) and (prev_occupation.room == room):
                json['msg'] = 'Mieszkasz w tym pokoju.'
                json['buttons'] = CONST_OK_BTN + CONST_LEAVE_ROOM_BTN
            elif (prev_occupation is None):
                get_in_room(request.user, room)
                json['msg'] = u"<br/>Właśnie dołączyłeś do tego pokoju<br/>"
                json['buttons'] = CONST_OK2_BTN + CONST_LEAVE_ROOM_BTN
            else: # prev_occ and not in this room
                json['msg'] = u"<br/>Jeśli chcesz się dopisać do tego pokoju,<br/>musisz najpierw opuścić pokój %s.<br/>" % prev_occupation.room
                json['buttons'] = CONST_OK_BTN
    elif status == 1:
        #
        # this room is locked or has password
        #
        if prev_occupation and (prev_occupation.room == room):
            json['msg'] = u"<br/>Zamknięty kluczem: <strong>%s</strong><br/>" % room.password
            json['buttons'] = CONST_OK_BTN + CONST_LEAVE_ROOM_BTN
        elif not prev_occupation:
            json['msg'] = u"<br/>Ten pokój jest zamknięty.<br/><input id='in_key' type='text' maxlength='6' size='6'></input><button onclick=\'Rooms.tryGetIn(%s)\'>Dopisz się</button>" % room.id
            json['buttons'] = u"<button onclick=\'hideDialog()\'>Anuluj</button>"
        else: # prev_occ and not in this room
            json['msg'] = u"<br/>Ten pokój jest zamknięty kluczem. Ponadto jeśli chcesz się do niego dopisać musisz najpierw opuścić pokój %s.<br/>" % prev_occupation.room
            json['buttons'] = CONST_OK_BTN
    elif status == 2: # room is full
        #
        # TODO: opcja do wypisania sie?
        #
        json['msg'] = u"<br/>Ten pokój jest już pełny.<br/>"
        json['buttons'] = CONST_OK_BTN
        if prev_occupation and (prev_occupation.room == room):
	    json['buttons'] = CONST_OK_BTN + CONST_LEAVE_ROOM_BTN
    #
    elif status == 3:
        json['msg'] = u"<br/>Zapisy na pokoje są jeszcze zamknięte.<br/>"
        json['buttons'] = CONST_OK_BTN
    json['locators'] = get_room_locators(room)
    return HttpResponse(dict_to_json(json), mimetype="application/json")

