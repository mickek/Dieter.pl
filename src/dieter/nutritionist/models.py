# -*- coding: utf-8 -*-    

from django.db import models
from django.contrib.auth.models import User

class PrivatePractice(models.Model):
    
    name = models.CharField('Nazwa gabinetu', max_length=300)
    
    '''
    Used when user registrating for this private practice
    '''
    registration_code = models.CharField('Kod affiliate', max_lenth=10, nullable=True, blank=True)
    
    # todo dodaj sensowne pola na adres, miasto i kod pocztowy
    
    # todo dodaj nip i regon
    
    # todo jak rozwiązać kwestie dietetyków? Własna klasa dziedzicząca po User? Potrzeba stworzenia migracji kopiującej dane z auth_user do patients_user
    
    # todo rozwiązać kwestie uprawnień, regionem będą gabinety i sam serwis
    
    pass