# -*- coding: UTF-8 -*-

from django.utils.translation import ugettext as _
from django import forms
from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm

class LoginForm(forms.Form):
    email     = forms.EmailField(required=True)
    password  = forms.CharField(widget=forms.PasswordInput())

class ValidatedPasswordChangeForm(PasswordChangeForm):
    new_password1 = forms.CharField(label=("New password"), widget=forms.PasswordInput)

    def clean_new_password1(self):
        password1 = self.cleaned_data.get(_('new_password1'))
        if len(password1) < 6:
            raise forms.ValidationError(_("Password too short"))
        return password1
