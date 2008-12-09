# -*- coding: UTF-8 -*-
from django.db import models

class Room(models.Model):
    number = models.CharField(max_length=16)
    capacity = models.PositiveIntegerField(max_length=1) # burżuje jesteśmy :P
    # locators
    # password
    # unlock_time

