# -*- coding: UTF-8 -*-
from datetime import datetime

# TODO: this module should be replaced by calls to database

def is_registration_enabled():
	# this is the only place that should be changed
	start_date = datetime(2011,2,2, 1,05)
	final_date = datetime(2011,2,24, 1,05)
	assert start_date < final_date
	return datetime.now() > start_date and datetime.now() < final_date


def is_registration_disabled():
	return not is_registration_enabled()


def is_lecture_suggesting_enabled():
	# this is the only place that should be changed
	start_date = datetime(2011,2,2, 1,05)
	final_date = datetime(2011,2,24, 1,05)
	assert start_date < final_date
	return datetime.now() > start_date and datetime.now() < final_date


def is_lecture_suggesting_disabled():
	return not is_lecture_suggesting_enabled()


def is_rooming_enabled():
	start_date = datetime(2011,2,26, 20,00)
	final_date = datetime(2011,3,1, 20,00)
	assert start_date < final_date
	return datetime.now() > start_date and datetime.now() < final_date


def is_rooming_disabled():
	return not is_rooming_enabled()

