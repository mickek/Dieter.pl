# -*- coding: utf-8 -*-    
from django.db import models
from django.contrib.auth.models import User
from dieter.utils import DieterException
from dieter.console import strfix
import datetime

class DietManager(models.Manager):
    """
    When creating diet we should also create dayplan objects.
    """
    def create(self, **kwargs):

        diet_length = kwargs['length'] if 'length' in kwargs else 21
        del kwargs['length']        
        new_diet = self.get_query_set().create(**kwargs)

        for i in range(1,diet_length):
            new_diet.dayplan_set.create(sequence_no=i)
            
        return new_diet
    
    def get_or_create(self, **kwargs):

        diet_length = kwargs['length'] if 'length' in kwargs else 21        
        diet, created = self.get_query_set().get_or_create(**kwargs)
        del kwargs['length']
        if created:

            for i in range(1,diet_length): diet.dayplan_set.create(sequence_no=i)
            diet.save()
            
        return (diet, created,)
    
class Diet(models.Model):

    STATE_CHOICES = (
        ('active', 'aktywna'),
        ('inactive', 'nieaktywna'),
    )
    
    TYPE_CHOICES = (
        ('user_created', 'Stworzona przez użytkownika'),
        ('nutronist_created', 'Stworzona przez dietetyka'),
        ('for_sale', 'Na sprzedaż'),
        ('for_free', 'Darmowa'),
    )    

    name            = models.CharField('Nazwa diety', max_length=200, null=True, blank=True) # used for displaying diets
    description     = models.TextField('Opis diety', max_length=50000, null=True, blank=True)
    
    start_date      = models.DateField('Data startu diety',null=True,blank=True)

    state           = models.CharField('Stan diety', max_length=50, choices=STATE_CHOICES, null=True, blank=True)   # may be active / inactive diet is inactive when it's created but not yet sent to patient
    type            = models.CharField('Typ diety', max_length=50, null=True, blank=True, choices=TYPE_CHOICES) # may be 'user_created', 'nutronist_created', 'for_sale', 'for_free'
    
    user            = models.ForeignKey(User, null=True, blank=True)
    
    '''
    Dieta na podstawie, której powstała ta dieta.
    Podczas wyboru / kupna diety ustawimy odpowiednia wartosc 
    '''
    parent          = models.ForeignKey('self', null=True, blank=True, related_name='parent_diet')
    '''
    Cena diety, powinna byc ustalona tylko jesli dieta jest typu: for_sale
    '''
    price           = models.FloatField('Cena', null=True, blank=True)
    
    objects         = DietManager()
    
    def __unicode__(self):
        return strfix("Diet[%s] %s" % (self.pk, self.name))
    
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
            diet_length = len(self.dayplan_set.all())-1
            return self.start_date + datetime.timedelta(days=diet_length)
        else: return None
        
    def current_day_plan(self, day):

        day_plan = None
        if self.start_date:
            if day >= self.start_date and day <= self.end_day():
                day_no = (day - self.start_date).days+1
                
                day_plan = self.dayplan_set.get(sequence_no=day_no) 
        else:
            day_plan = self.dayplan_set.get(sequence_no=1)

        return day_plan
        
        
    
class DayPlan(models.Model):
    
    """
    Sequence number starts from 1
    """
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
        
    def expected_day(self):
        if self.diet.start_date:
            return self.diet.start_date + datetime.timedelta(days=self.sequence_no-1)
        else: return None        
        
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
        
    def __str__(self):
        return self.name
            
    
        
class Food(models.Model):
    
    name            = models.CharField('Typ posiłku', max_length=100, null=False)
    calories        = models.FloatField('Liczba kalorii', default=1)
    unit_type       = models.CharField('Typ jednostki',max_length=50)
    
    def __str__(self):
        return self.name