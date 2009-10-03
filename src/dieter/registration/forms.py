# -*- coding: utf-8 -*-    

from django import forms
from django.contrib.auth.models import User
from registration.models import RegistrationProfile
from dieter.patients.models import Coupon
import re

attrs_dict = { 'class': 'required' }

class RegistrationForm(forms.Form):

    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=75)),
                             label=u'Adres email:')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=u'Hasło:')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=u'Hasło (powtórz):')
    
    #coupon  = forms.RegexField(regex="[0-9]+", label=u'Kupon promocyjny', required=False)
    
    tos = forms.BooleanField(widget=forms.CheckboxInput(attrs=attrs_dict), label='Przeczytałem i zgadzam się na regulamin serwisu:')

    def clean_email(self):
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError('Ten adres email, jest zajęty proszę wprowadź inny')
        return self.cleaned_data['email']
    
    def clean_tos(self):
        if self.cleaned_data.get('tos', False):
            return self.cleaned_data['tos']
        raise forms.ValidationError(u'Muisz wyrazić zgoę aby się zarejestrować')
    
    
    def save(self, profile_callback=None):
        
        new_user = RegistrationProfile.objects.create_inactive_user(username= re.sub(r"[@\-+.]", "_", self.cleaned_data['email']),
                                                                    password= self.cleaned_data['password1'],
                                                                    email= self.cleaned_data['email'])
        
        if 'coupon' in self.cleaned_data and self.cleaned_data['coupon']:
            coupon = Coupon(user=new_user,coupon=self.cleaned_data['coupon'])
            coupon.save()
        
        return new_user