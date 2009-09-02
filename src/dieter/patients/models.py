# -*- coding: utf-8 -*-    

from django.db import models
from django.contrib.auth.models import User
from dieter.utils import today_tommrow

class Profile(models.Model):
    
    GENDER_CHOICES = (
        (1, 'Męzczyzna'),
        (2, 'Kobieta'),
    )
    
    sex             = models.PositiveSmallIntegerField('Płeć', choices=GENDER_CHOICES, blank=False, null=True)
    height          = models.FloatField('Wzrost', null=True, blank=False)
    target_weight   = models.FloatField('Waga docelowa',null=True, blank=False)
    
    user            = models.ForeignKey(User, unique=True)
    
    def has_diet(self):
        return len(self.user.diet_set.all())
    
    def current_diet(self):
        return self.user.diet_set.all()[0]
    
    def is_profile_complete(self):
        """
        >>> p = Profile()
        >>> p.is_profile_complete()
        False
        >>> p = Profile(height = 176.8, target_weight = 86.5 )
        >>> p.is_profile_complete()
        False
        >>> p = Profile(sex = 1, height = 176.8, target_weight = 86.5 )
        >>> p.is_profile_complete()
        True
        """
        return self.height is not None and self.target_weight is not None and self.sex is not None
    
    def get_current_data(self):
        
        today, tommorow = today_tommrow()
        data = self.user.userdata_set.filter(date__gte=today, date__lte=tommorow)

        if data:
            return data[0]
        else:
            # get the latest data
            data = self.user.userdata_set.all().order_by('-date')[:1]
            if data:
                return UserData(user=self.user, weight=data[0].weight, waist=data[0].waist)
            else:
                return UserData(user=self.user)
        

class Coupon(models.Model):
    
    coupon  = models.CharField('Numer', max_length=20, null=False, unique=True)
    user    = models.ForeignKey(User, unique=True)
    
class UserData(models.Model):
    
    waist   = models.FloatField('Obwód pasa/tailii', null=True)
    weight  = models.FloatField('Waga', null=False)
    date    = models.DateField('Data', auto_now=True)    
    
    user    = models.ForeignKey(User)
        