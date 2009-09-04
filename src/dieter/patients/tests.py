from unittest import TestCase
from dieter.patients.utils import approximate_user_data
from dieter.patients.models import UserData
import datetime


class ValueDifferenceTests(TestCase):
    
    def test_approximate_user_data(self):
        
        date_to = datetime.datetime(day=14,month=1,year=2009)
        date_from = date_to - datetime.timedelta(days=23)
        
        udl = []
                
        for i in [1,2,3,4,11,12,13,14,20,21,22,23,24,25,26]:

            udl.append(UserData(
                                weight=0 if i in [1,2,24,25,26] else 90 - i*0.5,
                                date=date_from+datetime.timedelta(days=i))
            )
        
        approximate_user_data(udl)