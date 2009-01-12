# -*- coding: UTF-8 -*-

from django.db import models
from django.contrib.auth.models import User

from datetime import datetime

class LectureManager(models.Manager):

    def create_lecture(self, new_data, user):
        data = new_data.cleaned_data
        lecture = self.model( author    = user,
                              title     = data['title'],
                              duration  = data['duration'],
                              abstract  = data['abstract'],
                              info      = data['info'],
                              date_time = datetime.now(),
                              accepted  = False
                            )
        lecture.save()
        return lecture


class Lecture(models.Model):
    title     = models.CharField(max_length=128)
    duration  = models.PositiveIntegerField(max_length=3)
    abstract  = models.TextField(max_length=512)
    info      = models.TextField(max_length=2048)
    #dodatkowe info dla organizatorów
    author    = models.ForeignKey(User)
    date_time = models.DateTimeField()
    accepted  = models.BooleanField()

    objects = LectureManager()

    def __unicode__(self):
        return u"%s - %s" % (self.author, self.title)
        
