# -*- coding: utf-8 -*-

from django import forms
from django.forms.models import ModelForm
from dieter.diet.models import Diet

class CreateDietForm(ModelForm):

    name        = forms.CharField(required=True, label='Nazwa')
    type        = forms.ChoiceField(required=True, label="Typ diety", choices=Diet.TYPE_CHOICES)
    diet_length = forms.IntegerField(label='Długość diety', required=True)

    def clean_price(self):
        '''
        Diety 'for_sale' muszą mieć uzupełnioną cenę
        '''
        if self.cleaned_data['type'] == 'for_sale' and self.cleaned_data['price'] is None:
            raise forms.ValidationError('Musisz podać cenę diety jeśli wybrałeś typ diety: "Na sprzedaż"')
        return self.cleaned_data['price']

    class Meta:
        model = Diet
        fields = ('name','description','type','price')
