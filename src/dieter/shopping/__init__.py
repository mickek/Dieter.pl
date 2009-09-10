from dieter.utils import calculate_similarity
from dieter.console import write
import collections
import re
from dieter.diet.models import Food
 

"""
Merges meals into food ( cost of not having exact data structures )
Tries to find best match, returns matched foods, unmatched foods, and debug with probobalities of matched foods
"""
def agregate_meal_data( meals ):
    
    food = Food.objects.all()
    
    recognized_food = collections.defaultdict(float)
    not_recognized = collections.defaultdict(dict)
    matches_debug = []

    for meal in meals:
        
        matches = [ (calculate_similarity(meal.name, f.name), f,) for f in food ]   # similarity function
        matches.sort(cmp = lambda a,b: cmp(a[0],b[0]), reverse=True)
        
        first_match_probability, first_match = matches[0]
        
        if first_match_probability: # there's match even slight > 0.0
            recognized_food[first_match] += meal.quantity
            matches_debug.append((matches[0], meal,))
        else:   # no match at all
            if meal.name.lower() in not_recognized:
                if meal.quantity:
                    not_recognized[meal.name.lower()]['quantity'] += meal.quantity
            else:
                not_recognized[meal.name.lower()] = {'quantity':meal.quantity, 'unit_type': meal.unit_type}
            
    return {
            'recognized':recognized_food.items(), 
            'not_recognized': not_recognized.items(),
            'debug':matches_debug
    }

