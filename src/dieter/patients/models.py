# -*- coding: utf-8 -*-    

from django.db import models
from django.contrib.auth.models import User
from dieter.utils import today
from dieter.patients import approximate_user_data_for_date
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
        if no other user_data is in the db it sets weight and waist to 0,
        else it sets weigth and waist to values from the latest user_data 
        """
        try:
            data = self.user.userdata_set.get(date=day)
            return data
        except UserData.DoesNotExist:
            # get the latest data
            approximated_weight = approximate_user_data_for_date(self.user.userdata_set.all(),"weight",day)
            if not approximated_weight: approximated_weight = 0
            return UserData(user=self.user, weight=approximated_weight, waist=0, date=day)
            
    def __getattr__(self, name):
        if name.startswith("diff"):
            type, param, number, unit = name.split("_")
            if type == "diff": return self.get_diff(today(), param, int(number), unit)
        else:
            return super.__getattr__(name)
    
    def get_diff(self, end, param, number, unit):
        
        params = {}
        
        if unit.startswith("day"): params['days'] = number
        if unit.startswith("week"): params['weeks'] = number
        if unit.startswith("month"): 
            params['days'] = number*30            
        if unit.startswith("year"): 
            params['days'] = number*365
        
        start = end - datetime.timedelta(**params)
        
        start_val = approximate_user_data_for_date(self.user.userdata_set.all(),param,start)
        end_val = approximate_user_data_for_date(self.user.userdata_set.all(),param,end)

        if end_val and start_val:
            return end_val - start_val
        else: return None

class Coupon(models.Model):
    
    coupon  = models.CharField('Numer', max_length=20, null=False, unique=True)
    user    = models.ForeignKey(User, unique=True)
    
class UserData(models.Model):
    
    waist   = models.FloatField('Obwód pasa/tailii', null=True)
    weight  = models.FloatField('Waga', null=False)
    date    = models.DateField('Data', default=datetime.datetime.now)    
    
    user    = models.ForeignKey(User)
    
    @property
    def bmi(self):
        return (self.weight / (self.user.get_profile().height/100.)**2)

    def __cmp__(self, other):                       
        if isinstance(other, UserData):            
            return cmp(self.date, other.date)      
        else:                                     
            return cmp(self, other)

    
    def __unicode__(self):
        return "%s: %s kg" % (self.date, self.weight)
    
    
def user_post_save(sender, instance, **kwargs):
    Profile.objects.get_or_create(user=instance)

models.signals.post_save.connect(user_post_save, sender=User)

        