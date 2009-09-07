# -*- coding: utf-8 -*-    
from django.db import models
from django.contrib.auth.models import User
from dieter.utils import DieterException
import datetime

class DietManager(models.Manager):
    
    def create(self, **kwargs):
        
        new_diet = self.get_query_set().create(**kwargs)
        for i in range(1,21):
            new_diet.dayplan_set.create(sequence_no=i)
            
        return new_diet
    
    def get_or_create(self, **kwargs):
        
        diet, created = self.get_query_set().get_or_create(**kwargs)
        if created:
            for i in range(1,21): diet.dayplan_set.create(sequence_no=i)
            diet.save()
            
        return (diet, created,)
    
class Diet(models.Model):
    
    start_date      = models.DateField('Data startu diety',null=True,blank=True)
    state           = models.CharField('Stan diety', unique=False, max_length=50)
    
    user            = models.ForeignKey(User)
    
    objects         = DietManager()
    
    def add_day(self, sequence_no):

        if sequence_no is None:
            max_day = max(self.dayplan_set.all())
            day = 1 if max_day is None else max_day.sequence_no+1 
        else:
            raise DieterException("Adding days in between not implemented")
    
        self.dayplan_set.create(sequence_no=day)
        self.save()
        return day        
        
    def remove_day(self, sequence_no):
        
        if len(self.dayplan_set.all())<2: raise DieterException("Can't remove all days from diet")

        """
        Remove day
        """
        if sequence_no is None:
            current_day = min(self.dayplan_set.all())
        else:
            current_day = self.dayplan_set.get(sequence_no=sequence_no)

        sequence_no = current_day.sequence_no
        current_day.delete()
    
        """
        Cleanup
        """
        for i, d in enumerate(self.dayplan_set.all()):
            d.sequence_no = i+1
            d.save()
        
        if sequence_no > 1: sequence_no -= 1 
        return sequence_no
    
    def end_day(self):
        if self.start_date:
            diet_length = len(self.dayplan_set.all())
            return self.start_date + datetime.timedelta(days=diet_length)
        else: return None
        
    
class DayPlan(models.Model):
    
    sequence_no     = models.IntegerField('Liczba porządkowa')
    diet            = models.ForeignKey(Diet)
    
    def __cmp__(self, other):                       
        if isinstance(other, DayPlan):            
            return cmp(self.sequence_no, other.sequence_no)      
        else:                                     
            return cmp(self, other)
        
    def __getattr__(self, name):
        if name.startswith("meal"):
            _, meal = name.split("_")
            return self.meal_set.filter(type=meal)
        else:
            return super.__getattr__(name)
        
        
    class Meta:
        ordering = ["sequence_no"]    

class Meal(models.Model):
    
    type            = models.CharField('Typ posiłku', max_length=100, null=False)
    name            = models.CharField('Nazwa dania', max_length=250, null=False)
    quantity        = models.FloatField('Ilość', null=True)
    sequence_no     = models.IntegerField('Liczba porządkowa')
    unit_type       = models.CharField('Typ jednostki',max_length=50, null=True)
    
    day             = models.ForeignKey(DayPlan)
    
    def __cmp__(self, other):                       
        if isinstance(other, Meal):            
            return cmp(self.sequence_no, other.sequence_no)      
        else:                                     
            return cmp(self, other)
        
    class Meta:
        ordering = ["sequence_no"]    
    
        
class Food(models.Model):
    
    name            = models.CharField('Typ posiłku', max_length=100, null=False)
    calories        = models.FloatField('Liczba kalorii', default=1)
    unit_type       = models.CharField('Typ jednostki',max_length=50)
