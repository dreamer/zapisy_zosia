# -*- coding: UTF-8 -*-

from django import forms 

class LoginForm(forms.Form):
    email     = forms.EmailField(required=True)
    password  = forms.CharField(widget=forms.PasswordInput())

