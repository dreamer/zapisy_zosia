# -*- coding: UTF-8 -*-
from django.db import models
from datetime import datetime

class ZosiaDefinition(models.Model):
    active_definition			= models.BooleanField()
    # dates
    registration_start			= models.DateTimeField()
    registration_final			= models.DateTimeField()
    payment_deadline            = models.DateTimeField()
    lectures_suggesting_start	= models.DateTimeField()
    lectures_suggesting_final	= models.DateTimeField()
    rooming_start				= models.DateTimeField()
    rooming_final				= models.DateTimeField()
    zosia_start                 = models.DateTimeField()
    zosia_final                 = models.DateTimeField()
    # prices
    price_overnight             = models.IntegerField()
    price_overnight_breakfast   = models.IntegerField()
    price_overnight_dinner      = models.IntegerField()
    price_overnight_full        = models.IntegerField()
    price_transport             = models.IntegerField()
    price_organization          = models.IntegerField()
    # bank account
    account_number              = models.CharField(max_length=30)
    account_data_1              = models.CharField(max_length=40)
    account_data_2              = models.CharField(max_length=40)
    account_data_3              = models.CharField(max_length=40)
    # place
    city                        = models.CharField(max_length=20)
    city_c                      = models.CharField(max_length=20, verbose_name="miasto w celowniku")
    city_url                    = models.URLField()
    hotel                       = models.CharField(max_length=30)
    hotel_url                   = models.URLField()
    