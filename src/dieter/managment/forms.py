# -*- coding: utf-8 -*-

from django import forms
from django.forms.models import ModelForm
from dieter.diet.models import Diet

class CreateDietForm(ModelForm):

    diet_length = forms.IntegerField(label='Długość diety')

    class Meta:
        model = Diet
        fields = ('name','description','type','price')
