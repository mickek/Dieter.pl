# -*- coding: utf-8 -*-

from django.forms.models import ModelForm
from dieter.patients.models import Profile
from django import forms


class ProfileForm(ModelForm):

    current_weight = forms.FloatField(label="Aktualna waga")
    current_waist = forms.FloatField(label="Aktualny obwód pasa")  

    class Meta:
        model = Profile
        exclude = ('user',)
