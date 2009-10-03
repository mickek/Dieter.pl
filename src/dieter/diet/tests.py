# -*- coding: utf-8 -*- 

from unittest import TestCase
from dieter.diet import parse_quantity
from dieter.patients.models import user_post_save
from django.contrib.auth.models import User
from django.db import models

'''
Required or the user_post_save signall will cause column user_id is not unique error
'''
models.signals.post_save.disconnect(user_post_save, User)

class ParseQuantityTest(TestCase):
    
    def test_whitespace(self):
        
        q, t = parse_quantity("1 szklanka")
        self.assertEquals(q,1)
        self.assertEquals(t,"szklanka")
        
        q, t = parse_quantity("2 szklanki")
        self.assertEquals(q,2)
        self.assertEquals(t,"szklanki")
        
        q, t = parse_quantity("2 kromka")
        self.assertEquals(q,2)
        self.assertEquals(t,"kromka")        
        
        q, t = parse_quantity("2 kromki")
        self.assertEquals(q,2)
        self.assertEquals(t,"kromki") 

    def test_no_whitespace(self):
        
        q, t = parse_quantity("100g")
        self.assertEquals(q,100)
        self.assertEquals(t,"g")
        
    def test_just_numbers(self):
        
        q, t = parse_quantity("100")
        self.assertEquals(q,100)
        self.assertEquals(t,None)
        
    def test_floats(self):
        
        q, t = parse_quantity("100.0 g")
        self.assertEquals(q,100)
        self.assertEquals(t,'g')
        
    def test_invalid(self):
        
        q, t = parse_quantity("xyz")
        self.assertEquals(q,None)
        self.assertEquals(t,None)
        
    def test_polish_letters(self):
        q, t = parse_quantity("5 plasterków")
        self.assertEquals(q,5)
        self.assertEquals(t,"plasterków")
        
    def test_none(self):
        q, t = parse_quantity("")
        self.assertEquals(q,None)
        self.assertEquals(t,None)
        
        
        