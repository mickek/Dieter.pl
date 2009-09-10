from django.test import TestCase
from dieter.diet.models import Meal
from dieter.shopping import agregate_meal_data


class FoodAgregationTest(TestCase):
    
    fixtures = ['full_diet.json']

    def test_day_agregation(self):
        
        meals = Meal.objects.filter(sequence_no=1)
        d = agregate_meal_data(meals)
        print d['debug']
        print d['recognized']
        print d['not_recognized']
    
    def test_week_agregation(self):
        
        meals = Meal.objects.filter(sequence_no__range=(1,7))
        d = agregate_meal_data(meals)
        print d['debug']
        print d['recognized']
        print d['not_recognized']