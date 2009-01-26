# -*- coding: UTF-8 -*-
from datetime import datetime

def is_registration_disabled():
    # final date for registration
    # this is the only place that should be changed
    final_date = datetime(2009,1,27, 22,35)
    return datetime.now() > final_date

