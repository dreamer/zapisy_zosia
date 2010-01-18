# -*- coding: UTF-8 -*-
from datetime import datetime

# TODO: this module should be moved to common/
# ASAP

def is_registration_disabled():
    # final date for registration
    # this is the only place that should be changed
    final_date = datetime(2009,2,21, 1,15)
    return datetime.now() > final_date

def is_lecture_suggesting_disabled():
    # final date for registration
    # this is the only place that should be changed
    final_date = datetime(2009,3,2, 1,15)
    return datetime.now() > final_date

def is_lecture_suggesting_disabled():
    # final date for registration
    # this is the only place that should be changed
    final_date = datetime(2009,1, 28, 22,35)
    return datetime.now() > final_date

