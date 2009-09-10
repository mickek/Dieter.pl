from django.contrib.auth.decorators import login_required
from dieter.utils import profile_complete_required, today as get_today
from django.views.generic.simple import direct_to_template
from dieter.shopping import agregate_meal_data
from dieter.diet.models import Diet
import datetime
from django.http import HttpResponseNotFound

@login_required
@profile_complete_required
def index(request, mode = None):
    """
    shows shooping list for either X next days from ongoing diet 
    or X first days from a not started diet
    """
    try:
        meals = []
        today = get_today()
        diet = Diet.objects.get(user = request.user)
        day_range = 1 if mode is None or mode == 'day' else 7
        
        if diet.start_date: # there's a diet and the starting day has been choosen
            days = [ diet.current_day_plan(today + datetime.timedelta(days=i)) for i in range(day_range) ]
        else:   # there's a diet, but the starting day haven't been choosen
            days = diet.dayplan_set.get(sequence_no_range=(1,day_range))
        
        for d in days: meals.extend(d.meal_set.all())
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
    
        return direct_to_template(request, 'shopping/index.html', locals())
    
    except Diet.DoesNotExist: #@UndefinedVariable
        return HttpResponseNotFound ('<h1>Nie znaleziono diety</h1>')
    
@login_required
@profile_complete_required
def print_list(request, mode = None):
    return HttpResponseNotFound ('<h1>Nie znaleziono diety</h1>')
        
