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
    
class CreateDietForm(ModelForm):

    name        = forms.CharField(required=True, label='Nazwa')
    diet_length = forms.IntegerField(label='Długość diety', required=True)

    class Meta:
        model = Diet
        fields = ('name','description')
    