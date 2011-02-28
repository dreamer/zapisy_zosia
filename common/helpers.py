# -*- coding: UTF-8 -*-
from datetime import datetime, timedelta
from registration.models import UserPreferences

# TODO: this module should be replaced by calls to database

def is_registration_enabled():
	# this is the only place that should be changed
	start_date = datetime(2011,1,30, 1,05)
	final_date = datetime(2011,2,25, 1,05)
	assert start_date < final_date
	return datetime.now() > start_date and datetime.now() < final_date


def is_registration_disabled():
	return not is_registration_enabled()


def is_lecture_suggesting_enabled():
	# this is the only place that should be changed
	start_date = datetime(2011,1,30, 1,05)
	final_date = datetime(2011,2,25, 1,05)
	assert start_date < final_date
	return datetime.now() > start_date and datetime.now() < final_date


def is_lecture_suggesting_disabled():
	return not is_lecture_suggesting_enabled()


def is_rooming_enabled():
	start_date = datetime(2011,2,26, 20,00)
	final_date = datetime(2011,2,28, 23,00)
	assert start_date < final_date
	return datetime.now() > start_date and datetime.now() < final_date


def has_user_opened_records(user):
    prefs = UserPreferences.objects.get(user=user)
    user_openning_hour = datetime(2011,2,26, 20,00) - timedelta(minutes=prefs.minutes_early)
    return user_openning_hour <= datetime.now()


def is_rooming_disabled():
	return not is_rooming_enabled()

