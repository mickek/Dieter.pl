# -*- coding: utf-8 -*-    

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    
    GENDER_CHOICES = (
        (1, 'Męzczyzna'),
        (2, 'Kobieta'),
    )
    
    user    = models.ForeignKey(User, unique=True)
    
    sex  = models.PositiveSmallIntegerField(_(u'Płeć'), choices=GENDER_CHOICES, blank=True, null=True)
    height   = models.IntegerField(_(u'Wzrost'))
    target_weight   = models.IntegerField(_(u'Waga docelowa'))        
