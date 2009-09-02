# -*- coding: utf-8 -*-

from django.forms.models import ModelForm
from dieter.patients.models import UserData

class WeightForm(ModelForm):

    class Meta:
        model = UserData
        exclude = ('waist','date','user',)
