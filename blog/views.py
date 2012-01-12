# -*- coding: UTF-8 -*-

from django.http import *
from django.template import Context
from django.template.loader import get_template
from django.shortcuts import render_to_response

from common.forms import LoginForm
from common.models import ZosiaDefinition
from models import *

def main_view(view):
    def new_view(*args):
        locals = view(*args)
        locals['user']       = args[0].user
        locals['title']      = "Blog"
        locals['login_form'] = LoginForm()
        return render_to_response('blog.html',locals)
    return new_view

@main_view
def index(request):
    user = request.user
    blog_posts = BlogPost.objects.order_by('-pub_date')
    try:
        definition = ZosiaDefinition.objects.get(active_definition=True)
    except Exception:
        raise Http404
    registration_start          = definition.registration_start
    registration_final          = definition.registration_final
    lectures_suggesting_final   = definition.lectures_suggesting_final
    rooming_start               = definition.rooming_start
    rooming_final               = definition.rooming_final
    zosia_start                 = definition.zosia_start
    zosia_final                 = definition.zosia_final
    city                        = definition.city
    city_url                    = definition.city_url
    hotel                       = definition.hotel
    hotel_url                   = definition.hotel_url
    return locals()

