# -*- coding: utf-8 -*-    
from django.db import models

class PrivatePractice(models.Model):
    
    name = models.CharField('Nazwa gabinetu', max_length=300)
    
    '''
    Used when user registrating for this private practice
    '''
    registration_code = models.CharField('Kod affiliate', max_length=10, null=True, blank=True)
    
    '''
    Address data
    '''
    address = models.CharField('Adres',max_length=100, null=True, blank=True)
    postal_code = models.CharField('Kod Pocztowy',max_length=6, null=True, blank=True)
    city = models.CharField('Miasto',max_length=100, null=True, blank=True)
    province = models.CharField('Województwo',max_length=50, null=True, blank=True)

    '''
    Dane firmy wymagane do wystawiania faktur
    '''
    nip = models.CharField('NIP', max_length=13, null=True, blank=True)
    regon = models.CharField('Regon', max_length=15, null=True, blank=True)
    
    # todo rozwiązać kwestie uprawnień, regionem będą gabinety i sam serwis
    
    pass