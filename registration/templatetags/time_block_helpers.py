# -*- coding: UTF-8 -*-

from django import template
from registration.helpers import *
from django.utils.translation import ugettext as _

register = template.Library()

@register.simple_tag
def registration_link(x):
    if is_registration_disabled(): return ""
    p = '<li>'
    if x=="Registration": p = '<li id="current">'
    return p+'<a href="/register/">%s</a></li>' % _("Registration")

