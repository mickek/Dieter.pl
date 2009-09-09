# -*- coding: utf-8 -*-

from django.forms.models import ModelForm
from dieter.diet.models import Diet
from django import forms

class SetDietStartDateForm(ModelForm):

    class Meta:
        model = Diet
        fields = ('start_date',)
