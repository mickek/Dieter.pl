# -*- coding: utf-8 -*-    
from django.db import models
from django.contrib.auth.models import User

class Diet(models.Model):
    
    start_date      = models.DateField('Data startu diety',auto_now=True)
    state           = models.CharField('Stan diety', unique=False, max_length=50)
    
    user            = models.ForeignKey(User)


class DayPlan(models.Model):
    
    sequence_no     = models.IntegerField('Liczba porządkowa')
    diet            = models.ForeignKey(Diet)
    
    def __cmp__(self, other):                       
        if isinstance(other, DayPlan):            
            return cmp(self.sequence_no, other.sequence_no)      
        else:                                     
            return cmp(self, other)
        
    class Meta:
        ordering = ["sequence_no"]    

class Meal(models.Model):
    
    type            = models.CharField('Typ posiłku', max_length=100, null=False)
    name            = models.CharField('Nazwa dania', max_length=250, null=False)
    quantity        = models.FloatField('Ilość', default=1)
    sequence_no     = models.IntegerField('Liczba porządkowa')
    unit_type       = models.CharField('Typ jednostki',max_length=50)
    
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
