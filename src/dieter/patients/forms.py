# -*- coding: utf-8 -*-

from django.forms.models import ModelForm
from dieter.patients.models import Profile
from django import forms


class CompleteProfileForm(ModelForm):

    current_weight = forms.FloatField(label="Aktualna waga")
    current_waist = forms.FloatField(label="Aktualny obwód pasa", required=False)  

    class Meta:
        model = Profile
        exclude = ('user',)
        
class ProfileSettingsForm(ModelForm):

    class Meta:
        model = Profile
        exclude = ('user',)
        
        
        
