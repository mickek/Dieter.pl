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

def agregate_and_preprocess_meal_data(meals):
    
        aggregated_data = agregate_meal_data(meals)
        
        shooping_list = []
        shopping_list_other = []
        
        for food, quantity in aggregated_data['recognized']:
            if quantity: shooping_list.append((food.name, quantity, food.unit_type ))
            else: shopping_list_other.append(food.name)
            
        for food_name, data in aggregated_data['not_recognized']:
            if data['quantity']: 
                shooping_list.append((food_name, data['quantity'], data['unit_type']))
            else: shopping_list_other.append(food_name)
        
        shooping_list.sort(cmp=lambda a,b: cmp(a[0], b[0]))
        shopping_list_other.sort()   
        
        return shooping_list, shopping_list_other         
