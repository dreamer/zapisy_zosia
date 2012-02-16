# -*- coding: UTF-8 -*-

from django import template
from django.utils.translation import ugettext as _
from common.helpers import *

register = template.Library()

@register.simple_tag
def registration_link(x):
    if is_registration_disabled(): return ""
    p = '<li>'
    if x=="Registration": p = '<li id="current">'
    return p+'<a href="/register/">%s</a></li>' % _("Registration")


#FIXME move this helper to its own module
@register.simple_tag
def rooming_link(user,x):
    p = '<li>'
    if x=="Rooms": p = '<li id="current">'
    return p+'<a href="/rooms/">%s</a></li>' % "Zapisy na pokoje"
