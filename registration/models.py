# -*- coding: UTF-8 -*-

from django.db import models
from django.contrib.auth.models import User

# this is small hack to make user
# more meaningfull (we're using email as
# user id anyway)
User.__unicode__ = User.get_full_name

class Organization(models.Model):
    name = models.CharField(max_length=64)

class UserPreferences(models.Model):
    # This is the only required field
    user = models.ForeignKey(User, unique=True)

    # opłaty
    day_1 = models.BooleanField()
    day_2 = models.BooleanField()
    day_3 = models.BooleanField()

    breakfast_2 = models.BooleanField()
    breakfast_3 = models.BooleanField()
    breakfast_4 = models.BooleanField()

    dinner_1 = models.BooleanField()
    dinner_2 = models.BooleanField()
    dinner_3 = models.BooleanField()

    # inne
    bus         = models.BooleanField()
    vegetarian  = models.BooleanField()

    # ? anonimowy - nie chce zeby jego imie/nazwisko/mail pojawialy sie na stronie
    # ? wplacil   - zaplacil za... za Zosie+busa / sama zosie a busa osobno?

    def __str__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)


