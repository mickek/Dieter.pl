# -*- coding: utf-8 -*-

from django.test import TestCase
from dieter.patients.models import UserData, Profile, user_post_save
from dieter.patients import approximate_user_data,\
    approximate_user_data_for_date
from dieter.graphs.templatetags.graphs import weight_graph
import datetime
from django.contrib.auth.models import User
from django.db import models

'''
Required or the user_post_save signall will cause column user_id is not unique error
'''
models.signals.post_save.disconnect(user_post_save, User)

class ValueDifferenceTests(TestCase):
    
    fixtures = ['users.json','full_diet.json']    
    
    def test_approximate_user_data(self):
        '''
        Sprawdzamy czy approximate_user_data zwraca +- spodziewane wartosci
        '''
        
        date_to = datetime.date(day=14,month=1,year=2009)
        date_from = date_to - datetime.timedelta(days=23)
        
        udl = []
                
        for i in [1,2,3,4,11,12,13,14,20,21,22,23,24,25,26]:

            udl.append(UserData(
                                weight=0 if i in [1,2,24,25,26] else 90 - i*0.5,
                                date=date_from+datetime.timedelta(days=i))
            )
        self.assertEqual(26, len(approximate_user_data(udl,extend_to=26)))
        
    def test_approximate_user_data_for_day(self):
        '''
        Sprawdzamy czy approximate_user_data zwraca poprawne wartosci dla konkretnych dni
        '''
        date_to = datetime.date(day=14,month=1,year=2009)
        date_from = date_to - datetime.timedelta(days=23)
        
        udl = []
                
        for i in [1,2,3,4,11,12,13,14,20,21,22,23,24,25,26]:

            udl.append(UserData(
                                weight=0 if i in [1,2,24,25,26] else 90 - i*0.5,
                                date=date_from+datetime.timedelta(days=i))
            )
        

        self.assertEqual(88.5,approximate_user_data_for_date(udl, 'weight', datetime.date(day=23,month=12,year=2008)))
        
    def test_data_weight_graph_extend_both(self):
        '''
        Sprawdzamy czy weight_graph poprawnie rozszerza sie na prawo ( brak danych za ostantnie dni )
        i na lewo ( brak danych z zakresu początkowego )
        '''
        
        from django.utils import simplejson
        
        day = datetime.date(2009, 9, 4)
        user = User.objects.get(email='mklujszo@gmail.com')
        data =  weight_graph(user, day, 21, day)
             
        
        self.failIf(not data['plot_data'], 'plot_data can\'t be None')
        db_data = []
        db_data.extend(UserData.objects.filter( user=user).all())
        db_data.sort()

        
        for d in simplejson.loads(data['plot_data'])[0]:
            year,month,day = d[0].split("-")
            value = UserData.objects.filter( user=user, date = datetime.date(int(year), int(month), int(day) ) )
            
            #if value: 
            #    print "%s-%s-%s:\t%s\t\t%s" % (year, month, day, float(d[1]), value[0].weight)
            #else:
            #    print "%s-%s-%s:\t%s\t\t%s" % (year, month, day, float(d[1]), 'X')
             
            if len(value) > 0: self.failIf(float(d[1]) != value[0].weight, 'weight mismatch on: %s-%s-%s' % (year, month, day)) 
                    
    def test_data_weight_graph_no_extend_right(self):
        '''
        Sprawdzamy rozszerzerzanie się weight_graph tylko na lewo
        '''
        
        from django.utils import simplejson
        day = datetime.date(2009,9,7)
        
        user = User.objects.get(email='mklujszo@gmail.com')
        data =  weight_graph(user, day, 14, day)
        
        for d in simplejson.loads(data['plot_data'])[0]:
            year,month,day = d[0].split("-")
            value = UserData.objects.filter( user=user, date = datetime.date(int(year), int(month), int(day) ) )
             
            if len(value) > 0: self.assertEqual( float(d[1]), value[0].weight )
        
class ProfileTests(TestCase):
    
    fixtures = ['users.json','full_diet.json']    
    
    def test_custom_diff_getters(self):
        
        p = Profile.objects.get(user__email='mklujszo@gmail.com')
        p.diff_weight_1_week