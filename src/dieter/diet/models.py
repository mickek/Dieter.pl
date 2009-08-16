# -*- coding: utf-8 -*-    
from django.db import models
from django.contrib.auth.models import User

class Diet(models.Model):
    
    start_date      = models.DateField('Data startu diety',auto_now=True)
    state           = models.CharField('Stan diety', unique=False, max_length=50)
    
    user            = models.ForeignKey(User)
    
    """
    Always inserting in the end
    """
    def add_day(self, sequence_no):

        if sequence_no is None:
            max_day = max(self.dayplan_set.all())
            if max_day is None: day = 1
            else: day = max_day.sequence_no+1
        else:
            raise "Adding days in between not Implemented"
    
        self.dayplan_set.create(sequence_no=day)
        self.save()
        return True        
        
    def remove_day(self, sequence_no):
        
        if len(self.dayplan_set.all())<2: return False

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
