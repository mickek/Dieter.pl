from django.contrib.auth.decorators import login_required
from dieter.utils import profile_complete_required, today as get_today
from django.views.generic.simple import direct_to_template
from dieter.shopping import agregate_and_preprocess_meal_data
from dieter.diet.models import Diet
from django.shortcuts import get_object_or_404
import datetime

@login_required
@profile_complete_required
def agregated_meal_data(request, mode = 'day', template_name = 'index.html'):
    """
    shows shooping list for either X next days from ongoing diet 
    or X first days from a not started diet
    """
    meals = []
    today = get_today()
    diet = get_object_or_404(Diet, user=request.user, state = 'active')
    day_range = 1 if mode is None or mode == 'day' else 7
    
    if diet.start_date: # there's a diet and the starting day has been choosen
        days = [ diet.current_day_plan(today + datetime.timedelta(days=i)) for i in range(day_range) if diet.current_day_plan(today + datetime.timedelta(days=i)) is not None ]
    else:   # there's a diet, but the starting day haven't been choosen
        days = diet.dayplan_set.filter(sequence_no__range=(1,day_range))

    for d in days: meals.extend(d.meal_set.all())
    shooping_list, shopping_list_other = agregate_and_preprocess_meal_data(meals)

    return direct_to_template(request, 'shopping/%s' % template_name, locals())    