from django.forms.models import ModelForm
from dieter.patients.models import Profile
from django import forms


class ProfileForm(ModelForm):

    current_weight = forms.FloatField(label="Aktualna waga") 

    class Meta:
        model = Profile
        exclude = ('user',)
