# -*- coding: UTF-8 -*-

from django import forms 

ORG_CHOICES = (
    ('uwr', 'Uniwersytet Wrocławski'),
    ('ksi', 'Koło Studentów Informatyki'),
    ('new',   'other'),
)

SHIRT_SIZE_CHOICES = (
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
)

class RegisterForm(forms.Form):
    email    = forms.EmailField(required=True)
    password  = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    name    = forms.CharField()
    surname = forms.CharField()

    organization_1 = forms.ChoiceField(choices=ORG_CHOICES)
    # TODO: enable this
    #organization_2 = forms.ChoiceField(choices=ORG_CHOICES)
    #organization_3 = forms.ChoiceField(choices=ORG_CHOICES)

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
            raise forms.ValidationError("At least one day should be selected.")
    
    
