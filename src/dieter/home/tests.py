# -*- coding: utf-8 -*-

from django.test import TestCase
from dieter.patients.models import user_post_save
from django.contrib.auth.models import User
from django.db import models
from django.core import mail
import re

'''
Required or the user_post_save signall will cause column user_id is not unique error
'''
models.signals.post_save.disconnect(user_post_save, User)

class BasicFunctionsTest(TestCase):
    
    fixtures = ['users.json','full_diet.json', 'groups.json']
            
    def test_start_page(self):
        
        response = self.client.get("/")
        self.failIf(response.status_code != 200, 'home page didnt load')
        
    def test_login(self):
    
        self.client.post("/accounts/login/",{'username':'mklujszo@gmail.com','password':'test12'})
        
    def test_basic_services(self):
    
        self.client.login(username='mklujszo@gmail.com',password='test12')
        
        self.client.get("/dashboard/")
        self.client.get("/diet/")
        self.client.get("/inbox/")
        self.client.get("/graphs/")
        self.client.get("/graphs/week/")
        self.client.get("/graphs/month/")
        self.client.get("/graphs/all/")
        self.client.get("/shopping/")
        self.client.get("/shopping/week/")
        self.client.get("/settings/")
        self.client.get("/accounts/register/")        
        
class TestRegistration(TestCase):
    
    fixtures = ['groups.json']
    
    def setUp(self):
        
        models.signals.post_save.connect(user_post_save, sender=User)        
    
    
    def test_registration(self):

        '''
        Rejestracja
        '''
        self.client.post("/accounts/register/",{'email':'a@example.com','password1':'qaz123','password2':'qaz123', 'tos':'true'})
        
        self.assertEqual(len(mail.outbox), 1) #@UndefinedVariable
        
        results = re.findall(r'http://example.com/accounts/activate/([a-f0-9]*)\n', mail.outbox[0].body, re.MULTILINE)
        activation_key = results[0]
        
        self.failIf(not activation_key, 'no activation key')

        '''
        Aktywacja konta i logowanie
        '''        
        self.client.get('/accounts/activate/%s/' % activation_key)
        self.client.login(username='a@example.com',password='qaz123')
        
        '''
        Próba wejścia na dashboard
        '''        
        d =  self.client.get('/dashboard/')
        self.failIf(d['Location']!='http://testserver/complete_profile', 'after registration user should complete his profile')
        
        '''
        Uzupełnianie profilu
        '''        
        self.client.get('/complete_profile')
        self.client.post('/complete_profile',{'sex':'1','current_weight':'90','height':'160','target_weight':'76'})
        
        '''
        Wejście na dasboard
        '''
        self.client.get('/dashboard/')

        '''
        Sprawdzenie podstawowych funkcji
        '''
        self.client.get("/dashboard/")
        self.client.get("/diet/")
        self.client.get("/inbox/")
        self.client.get("/graphs/")
        self.client.get("/graphs/week/")
        self.client.get("/graphs/month/")
        self.client.get("/graphs/all/")
        self.client.get("/shopping/")
        self.client.get("/shopping/week/")
        self.client.get("/settings/")
        
    
        
    