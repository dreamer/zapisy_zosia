# -*- coding: UTF-8 -*-

from django.db import models
from django.contrib.auth.models import User

class Lecture(models.Model):
    title     = models.CharField(max_length=128)
    duration  = models.PositiveIntegerField(max_length=3)
    abstract  = models.TextField(max_length=2048)
    info      = models.TextField(max_length=2048, blank=True, null=True)
    #dodatkowe info dla organizatorów
    author    = models.CharField(max_length=128)
    #author    = models.ForeignKey(User, unique=False)
    date_time = models.DateTimeField()
    accepted  = models.BooleanField()

    def __str__(self):
        return "%s - %s" % ( self.title, "anonim")

    #class Meta:
    #    ordering = ["title"]

    #class Admin:
    #    list_display = ('title', 'author', 'duration', 'date_time')

