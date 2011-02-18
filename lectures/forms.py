# -*- coding: UTF-8 -*-

from django import forms 

class NewLectureForm(forms.Form):
    title = forms.CharField( max_length=128, required=True )
    duration = forms.ChoiceField(choices = ([(5,5), (15,15),(20,20),(25,25),(30,30), (45,45), (100,'inne')]),) 
    abstract = forms.CharField( widget=forms.Textarea(),
                                required=True, max_length=512 )
    sprezentujpl_email = forms.EmailField(required=False)
    info = forms.CharField( widget=forms.Textarea(),
                                required=False, max_length=2048 )
 
