# -*- coding: UTF-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.core.mail import send_mail
from django.template import Context, loader
from common.models import ZosiaDefinition
from datetime import timedelta

# this is small hack to make user
# more meaningfull (we're using email as
# user id anyway)
User.__unicode__ = User.get_full_name

SHIRT_SIZE_CHOICES = (
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
    ('XXL', 'XXL'),
    ('XXXL', 'XXXL'),
)

SHIRT_TYPES_CHOICES = (
    ('m', _('classic')),
    ('f', _('women')),
)

BUS_HOUR_CHOICES = (
    ('brak',''),
    ('16:00', '16:00'),
    ('18:00', '18:00'),
    ('obojetne', 'obojętne'),
)

BUS_FIRST_SIZE = 48
BUS_SECOND_SIZE = 48

class Organization(models.Model):
    name     = models.CharField(max_length=64)
    accepted = models.BooleanField()

    def __unicode__(self):
        return u"%s" % self.name

# converts organizations in database into
# choices for option fields
def getOrgChoices():
    list = [ (org.id, org.name)
           for org in Organization.objects.filter(accepted=True) ]
    list = list[:20]
    list.append( ('new', 'inna') )
    return tuple(list)

class UserPreferences(models.Model):
    # This is the only required field
    user = models.ForeignKey(User, unique=True)

    org = models.ForeignKey(Organization)

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
    # TODO(karol): remove after successfull verification that rest works.
    # paid_for_bus = models.BooleanField() # we need this after all :/
    shirt_size  = models.CharField(max_length=5, choices=SHIRT_SIZE_CHOICES)
    shirt_type  = models.CharField(max_length=1, choices=SHIRT_TYPES_CHOICES)

    # used for opening rooms faster per-user;
    # e.g. 5 means room registration will open 5 minutes before global datetime
    # e.g. -5 means room registration will open 5 minutes after global datetime
    # FIXME needs actual implementation, so far it's only a stub field
    minutes_early = models.IntegerField()


    # used to differ from times on which buses leave 
    bus_hour = models.CharField(max_length=10, choices=BUS_HOUR_CHOICES, null=True, default=None)

    # ? anonimowy - nie chce zeby jego imie/nazwisko/mail pojawialy sie na stronie
    
    def __unicode__(self):
        return u"%s %s" % (self.user.first_name, self.user.last_name)

    def save(self):
        # at this moment object probably is different from one in
        # database - lets check if 'paid' field is different
        try:
            old = UserPreferences.objects.get(id=self.id)
            definition = ZosiaDefinition.objects.get(active_definition=True)
            rooming_time = definition.rooming_start
            if self.paid and not old.paid:
                t = loader.get_template('payment_registered_email.txt')
                send_mail( u'Wpłata została zaksięgowana.',
                             t.render(Context({'rooming_time': rooming_time - timedelta(minutes=self.minutes_early)})),
                             'from@example.com',
                             [ self.user.email ],
                             fail_silently=True )
        except Exception:
            # oh, we're saving for the first time - it's ok
            # move along, nothing to see here
            pass
        super(UserPreferences, self).save() 


    @staticmethod
    def get_free_seats():
        return (BUS_SECOND_SIZE+BUS_FIRST_SIZE - UserPreferences.objects.filter(bus=True).count()) > 0

    @staticmethod
    def get_first_time():
        return  (BUS_FIRST_SIZE - UserPreferences.objects.filter(bus=True, bus_hour=BUS_HOUR_CHOICES[1][0]).count()) > 0

    @staticmethod
    def get_second_time():
        return  (BUS_SECOND_SIZE - UserPreferences.objects.filter(bus=True, bus_hour=BUS_HOUR_CHOICES[2][0]).count()) > 0