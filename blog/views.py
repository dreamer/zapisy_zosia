# -*- coding: UTF-8 -*-

from django.http import *
from django.template import Context
from django.template.loader import get_template
from django.shortcuts import render_to_response

from common.forms import LoginForm
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
    return locals()

