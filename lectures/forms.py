# -*- coding: UTF-8 -*-

from django import forms 

class NewLectureForm(forms.Form):
    title = forms.CharField( max_length=128, required=True )
    duration = forms.IntegerField( min_value=5, max_value=240 )
    abstract = forms.CharField( widget=forms.Textarea(),
                                required=True, max_length=512 )
    info = forms.CharField( widget=forms.Textarea(),
                                required=False, max_length=2048 )

