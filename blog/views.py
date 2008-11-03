# -*- coding: UTF-8 -*-

from django.http import *
from django.template import Context
from django.template.loader import get_template
from django.shortcuts import render_to_response

from models import *

def index(request):
    user = request.user
    blog_posts = BlogPost.objects.all()
    return render_to_response('blog.html',locals())

