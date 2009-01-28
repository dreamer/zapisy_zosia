# -*- coding: UTF-8 -*-

from django import forms 
from models import SHIRT_SIZE_CHOICES, SHIRT_TYPES_CHOICES
from models import getOrgChoices as organization_choices
from django.utils.translation import ugettext as _


def lambda_clean_meal(meal,p1,p2,p3,z):
    # ok, this if fuckin hacky function... so stay tuned
    # meal is name of field (without suffix) that we wanna validate
    # p1, p2, p3 are _pais_ of _numeral suffixes_ (meal_suffix, day_suffix)
    #
    # we return validator method for (field_3) validating
    # if meals are bought for respective hotel nights
    #
    # this field is reused several times, so its kinda
    # hacky path for DRY principle ;)
    #
    # usecase (in class body):
    #    clean_supper_3 = lambda_clean_meal('supper',(1,1),(2,2),(3,3))
    #
    def f(s):
        for n,d in [p1,p2,p3]:
            mealx = "%s_%s" % (meal,n)
            dayx  = "%s_%s" % ("day", d)
            x = s.cleaned_data.get(mealx)
            d = s.cleaned_data.get(dayx)
            if x and not d:
                raise forms.ValidationError(_("You can buy meal only for adequate hotel night."))
        return s.cleaned_data.get("%s_%i" % (meal,z))
    return lambda(s):f(s)


class RegisterForm(forms.Form):

    def __init__(self, *args, **kwargs) :
        super(forms.Form, self) .__init__(*args, **kwargs)
        self.fields['organization_1'].choices = organization_choices()

    email    = forms.EmailField(required=True)
    password  = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    name    = forms.CharField()
    surname = forms.CharField()

    organization_1 = forms.ChoiceField(choices=organization_choices())
    organization_2 = forms.CharField(required=False)

    day_1 = forms.BooleanField(required=False, initial=True)
    day_2 = forms.BooleanField(required=False, initial=True)
    day_3 = forms.BooleanField(required=False, initial=True)

    breakfast_2 = forms.BooleanField(required=False, initial=True)
    breakfast_3 = forms.BooleanField(required=False, initial=True)
    breakfast_4 = forms.BooleanField(required=False, initial=True)

    dinner_1 = forms.BooleanField(required=False, initial=True)
    dinner_2 = forms.BooleanField(required=False, initial=True)
    dinner_3 = forms.BooleanField(required=False, initial=True)

    vegetarian = forms.BooleanField(required=False)
    shirt_size = forms.ChoiceField(choices=SHIRT_SIZE_CHOICES)
    shirt_type = forms.ChoiceField(choices=SHIRT_TYPES_CHOICES)
    bus        = forms.BooleanField(required=False)

    def validate_nonempty(self,x):
        x = self.cleaned_data.get(x, '').strip()
        x = x.replace(' ','') # remove spaces
        # TODO: regex here!
        # [a-ż]+(-[a-ż]+)* for surnames ? ;)
        if len(x) == 0:
            raise forms.ValidationError("Be nice, fill this field properly.")
        return x

    def clean_name(self):
        return self.validate_nonempty('name')

    def clean_surname(self):
        return self.validate_nonempty('surname')

    def clean_password2(self):
        password = self.cleaned_data.get('password', '')
        password2 = self.cleaned_data.get('password2', '')
        if password != password2:
            raise forms.ValidationError("Ops, you made a typo in your password.")
        return password2

    def clean_password(self):
        password = self.cleaned_data.get('password', '')
        if len(password) < 6:
            raise forms.ValidationError("Password should be at least 6 characters long.")
        return password

    def clean_day_3(self):
        day1 = self.cleaned_data.get('day_1')
        day2 = self.cleaned_data.get('day_2')
        day3 = self.cleaned_data.get('day_3')
        if day1 or day2 or day3:
            return day3
        else:
            raise forms.ValidationError(_("At least one day should be selected."))
    
    clean_dinner_3    = lambda_clean_meal('dinner',    (1,1), (2,2), (3,3), 3 )
    clean_breakfast_4 = lambda_clean_meal('breakfast', (2,1), (3,2), (4,3), 4 )



# grrr, this REALLY should not be copied'n'pasted but
# correct form class hierarchy should be developed
# no time :(
class ChangePrefsForm(forms.Form):
    def __init__(self, *args, **kwargs) :
        super(forms.Form, self) .__init__(*args, **kwargs)
        self.fields['organization_1'].choices = organization_choices()[:-1]

    def add_bad_org(self,prefs):
        if not prefs.org.accepted:
            self.fields['organization_1'].choices.append( (prefs.org.id,prefs.org.name) )

    def initialize(self,prefs):
        # change values depending on given user preferences
        for key in prefs.__dict__.keys():
            if self.fields.has_key(key):
                self.fields[key].initial = prefs.__dict__[key]
        # organization selection
        self.add_bad_org(prefs)
        self.fields['organization_1'].initial = prefs.org.id

    organization_1 = forms.ChoiceField(choices=organization_choices())

    day_1 = forms.BooleanField(required=False)
    day_2 = forms.BooleanField(required=False)
    day_3 = forms.BooleanField(required=False)

    breakfast_2 = forms.BooleanField(required=False)
    breakfast_3 = forms.BooleanField(required=False)
    breakfast_4 = forms.BooleanField(required=False)

    dinner_1 = forms.BooleanField(required=False)
    dinner_2 = forms.BooleanField(required=False)
    dinner_3 = forms.BooleanField(required=False)

    vegetarian = forms.BooleanField(required=False)
    shirt_size = forms.ChoiceField(choices=SHIRT_SIZE_CHOICES)
    shirt_type = forms.ChoiceField(choices=SHIRT_TYPES_CHOICES)
    bus        = forms.BooleanField(required=False)

    paid = False
    def set_paid(self,b): self.paid = b

    def clean_day_3(self):
        day3 = self.cleaned_data.get('day_3')
        day1 = self.cleaned_data.get('day_1')
        day2 = self.cleaned_data.get('day_2')
        if day1 or day2 or day3 or self.paid:
            return day3
        else:
            raise forms.ValidationError(_("At least one day should be selected."))

    clean_dinner_3    = lambda_clean_meal('dinner',    (1,1), (2,2), (3,3), 3 )
    clean_breakfast_4 = lambda_clean_meal('breakfast', (2,1), (3,2), (4,3), 4 )


