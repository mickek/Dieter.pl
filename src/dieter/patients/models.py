# -*- coding: utf-8 -*-    

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    
    GENDER_CHOICES = (
        (1, 'Męzczyzna'),
        (2, 'Kobieta'),
    )
    
    sex  = models.PositiveSmallIntegerField('Płeć', choices=GENDER_CHOICES, blank=True, null=True)
    height   = models.IntegerField('Wzrost')
    target_weight   = models.IntegerField('Waga docelowa')
    
    user    = models.ForeignKey(User, unique=True)

class Coupon(models.Model):
    
    coupon  = models.CharField('Numer', max_length=20, null=False, unique=True)
    user    = models.ForeignKey(User, unique=True)