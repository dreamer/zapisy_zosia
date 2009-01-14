# -*- coding: UTF-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

# this is small hack to make user
# more meaningfull (we're using email as
# user id anyway)
User.__unicode__ = User.get_full_name

SHIRT_SIZE_CHOICES = (
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
)

SHIRT_TYPES_CHOICES = (
    ('m', _('classic')),
    ('f', _('women')),
)


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
    paid        = models.BooleanField()
    shirt_size  = models.CharField(max_length=2, choices=SHIRT_SIZE_CHOICES)
    shirt_type  = models.CharField(max_length=1, choices=SHIRT_TYPES_CHOICES)

    # ? anonimowy - nie chce zeby jego imie/nazwisko/mail pojawialy sie na stronie

    def __unicode__(self):
        return u"%s %s" % (self.user.first_name, self.user.last_name)
    


