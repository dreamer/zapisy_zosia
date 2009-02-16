# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import random

# most of non-standard fuss here is about serializing
# and caching rooms in database;
# this probably should be moved into different module
# for usage with built-in django serialization framework


class RoomManager(models.Manager):
    # this class does basic caching for json data
    # when any of room changes then flag update_required
    # should be set to True
    # this flag prevents database lookup for creating json data

    cache = ""
    update_required = True

    def to_json(self):
        if self.update_required:
            self.cache = [ x.to_json() for x in self.all() ]
            self.update_required = False
        return "[%s]" % (','.join(self.cache))


class NRoom(models.Model):
    number      = models.CharField(max_length=16)
    capacity    = models.PositiveIntegerField(max_length=1) # burżuje jesteśmy :P
    password    = models.CharField(max_length=16)
    #unlock_time         = models.DateTimeField()
    #short_unlock_time   = models.DateTimeField()

    # ok, this probably shouldn't be done this way, but proper one-to-many
    # relation requires changing user model which can't be done now
    # this should be refactored after ZOSIA09
    # locators = models.ManyToManyField(User, through='RoomMembership')
    objects = RoomManager()

    def to_json(self):
        no_locators = 0
        status = 0     # default; it's ok to sign into room
        if self.password != "":
            status = 1 # password is set
        if no_locators >= self.capacity:
            status = 2 # room is full
        # id - number
        # st - status
        # nl - number of locators
        # mx - max room capacity
        # features? (optional)
        #"""[{"id":"id","st":0,"nl":0,"mx":1}]"""
        return '{"id":"%s","st":%s,"nl":%s,"mx":%s}' % (self.number, 
                status, no_locators, self.capacity)

    def save(self):
        super(NRoom, self).save()
        # set cached data in manager to be updated
        self.__class__.objects.update_required = True


