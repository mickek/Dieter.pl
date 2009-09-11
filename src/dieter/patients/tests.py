from django.test import TestCase
from dieter.patients.models import UserData, Profile
from dieter.patients import approximate_user_data,\
    approximate_user_data_for_date
from dieter.utils import today
from dieter.dashboard.templatetags.graphs import weight_graph
import datetime
from django.contrib.auth.models import User


class ValueDifferenceTests(TestCase):
    
    fixtures = ['users.json','full_diet.json']    
    
    def test_approximate_user_data(self):
        
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
        
        from django.utils import simplejson
        
        day = today()
        user = User.objects.get(email='mklujszo@gmail.com')
        data =  weight_graph(user, day, 14, day)
        
        print 'today', day, 'length', len(simplejson.loads(data['plot_data'])[0])
        
        for d in simplejson.loads(data['plot_data'])[0]:
            year,month,day = d[0].split("-")
            value = UserData.objects.filter( user=user, date = datetime.date(int(year), int(month), int(day) ) )
            
            print d, value 
            if len(value) > 0: self.assertEqual( float(d[1]), value[0].weight )
            
        print 'today', simplejson.loads(data['plot_data'])[1]
        
    def test_data_weight_graph_no_extend_right(self):
        
        from django.utils import simplejson
        day = datetime.date(2009,9,7)

        
        user = User.objects.get(email='mklujszo@gmail.com')
        data =  weight_graph(user, day, 14, day)
        
        print 'today', day, 'length', len(simplejson.loads(data['plot_data'])[0])
        
        for d in simplejson.loads(data['plot_data'])[0]:
            year,month,day = d[0].split("-")
            value = UserData.objects.filter( user=user, date = datetime.date(int(year), int(month), int(day) ) )
            
            print d, value 
            if len(value) > 0: self.assertEqual( float(d[1]), value[0].weight )
            
        print 'today', simplejson.loads(data['plot_data'])[1]        

        
class ProfileTests(TestCase):
    
    def test_custom_diff_getters(self):
        
        p = Profile()
        
        print p.diff_weight_1_week