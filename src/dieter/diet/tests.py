# -*- coding: utf-8 -*- 

from django.test import TestCase
from dieter.diet import parse_quantity, copy_and_activate_diet
from dieter.patients.models import user_post_save
from django.contrib.auth.models import User
from django.db import models
from dieter.diet.models import Diet
from dieter.utils import DieterException

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
        
class DietCopierTest(TestCase):    
    
    fixtures = ['sample_diets.json']
    
    def test_simple_diet_copy(self):
        '''
        Generic diet to user without diet
        '''  
        
        target_user = User.objects.get(email = 'mklujszo+2@gmail.com')
        source_diet = Diet.objects.get( pk = 2 )
        
        copy_and_activate_diet(source_diet, target_user)
        
        try:
            
            diet = Diet.objects.get( user = target_user, state = 'active', parent = source_diet )
            self.failUnless(len(diet.dayplan_set.all()) == len(source_diet.dayplan_set.all()), 
                            "new(%s) and source diet(%s) have different dayplan length" % ( len(diet.dayplan_set.all()), len(source_diet.dayplan_set.all()) ))
            
            for i in range(1,len(source_diet.dayplan_set.all())):
                src_day = source_diet.dayplan_set.get(sequence_no = i)
                new_day = diet.dayplan_set.get(sequence_no = i)
                
                self.failUnless(len(src_day.meal_set.all()) == len(new_day.meal_set.all()), "day %s meals length missmatch" % i)
                
                for j in range(0,len(src_day.meal_set.all())):
                    src_meal = src_day.meal_set.get(sequence_no=j)
                    new_meal = new_day.meal_set.get(sequence_no=j)
                    
                    self.failIf(src_meal.name != new_meal.name, "name mismatch on meal %s in day %s" % (j,i))
                    self.failIf(src_meal.quantity != new_meal.quantity, "quantity mismatch on meal %s in day %s" % (j,i))
                    self.failIf(src_meal.type != new_meal.type, "type mismatch on meal %s in day %s" % (j,i))
                    self.failIf(src_meal.unit_type != new_meal.unit_type, "unit_type mismatch on meal %s in day %s" % (j,i))
                    
                    
                               
            
        except Diet.DoesNotExist: #@UndefinedVariable
            self.fail("no new diet with required conditions found")
        
    
    def test_diet_copy(self):
        '''
        Generic diet to user with diet
        deactivating old diet, activating new one
        '''
        
        target_user = User.objects.get(email = 'mklujszo+1@gmail.com')
        old_diet    = Diet.objects.get( user = target_user )
        source_diet = Diet.objects.get( pk = 2 )
        
        copy_and_activate_diet(source_diet, target_user)
        
        diets = Diet.objects.filter(user = target_user)
        self.failUnless(len(diets)==2, "target user should have two diets")
        
        old_diet = Diet.objects.get( pk = old_diet.pk )
        self.failUnless(old_diet.state == 'inactive', "old diet state must be inactive")
        
        new_diet = Diet.objects.get( user = target_user, state = 'active' )
        self.failUnless(new_diet.state == 'active', 'new diet has to be active')
        
    def test_invalid_diet_copy(self):
        
        target_user = User.objects.get(email = 'mklujszo+2@gmail.com')
        source_diet = Diet.objects.get( pk = 2 )
        
        copy_and_activate_diet(source_diet, target_user)
        
        try:
            copy_and_activate_diet(source_diet, target_user)
            self.fail("copy_and_activate_diet should have failed when trying to activate the same diet twice")
        except DieterException:
            pass

    
