# -*- coding: utf-8 -*-    

from django.db import models
from django.contrib.auth.models import User
from dieter.utils import today
import datetime

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
    
    def get_user_data(self,day=today()):
        """
        By default returns today's user data.
        If other date is set in day parameter tries to return that day user data.
        If no user data is created for this date it returns a new object, 
        if no other user_data is in the db it sets weight and waist set to 0,
        else it sets weigth and waist to values from the latest user_data 
        """
        try:
            data = self.user.userdata_set.get(date=day)
            return data
        except UserData.DoesNotExist:
            # get the latest data
            data = self.user.userdata_set.all().order_by('-date')[:1]
            if data:
                return UserData(user=self.user, weight=data[0].weight, waist=data[0].waist, date=day)
            else:
                return UserData(user=self.user, weight=0, waist=0, date=day)
        

class Coupon(models.Model):
    
    coupon  = models.CharField('Numer', max_length=20, null=False, unique=True)
    user    = models.ForeignKey(User, unique=True)
    
class UserData(models.Model):
    
    waist   = models.FloatField('Obwód pasa/tailii', null=True)
    weight  = models.FloatField('Waga', null=False)
    date    = models.DateField('Data', default=datetime.datetime.now)    
    
    user    = models.ForeignKey(User)
        