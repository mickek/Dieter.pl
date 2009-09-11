# -*- coding: utf-8 -*-

from django.forms.models import ModelForm
from dieter.diet.models import Diet
from django.forms.forms import Form
from django import forms

class SetDietStartDateForm(ModelForm):

    class Meta:
        model = Diet
        fields = ('start_date',)

class SendDietForm(Form):

    message = forms.CharField(max_length=300000,label='Opis diety', widget=forms.Textarea())