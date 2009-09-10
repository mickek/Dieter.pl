from django import template
from dieter.diet.models import DayPlan

register = template.Library()

def meals_section(context, type, name, meals):
    return { 'MEDIA_URL':context['MEDIA_URL'], 'meals': meals, 'name': name, 'type': type}

def meals_section_view(meals,name):
    return { 'meals': meals, 'name':name}

def day_plan(context, diet, day):
    """
    there is diet
       start day set
           day before start day
           day after start day
       start day not set
    or if day is an instance of dayplan we just show the dayplan    
    """


    day_plan = None
    if isinstance(day, DayPlan): day_plan = day
    else:
        if diet.start_date:
            if day >= diet.start_date and day <= diet.end_day():
                day_no = (day - diet.start_date).days+1
                
                day_plan = diet.dayplan_set.get(sequence_no=day_no) 
        else:
            # show first day of diet
            day_plan = diet.dayplan_set.get(sequence_no=1)
        
    return { 'day_plan': day_plan }

register.inclusion_tag('diet/meals_section.html', takes_context=True)(meals_section)
register.inclusion_tag('diet/day_plan.html', takes_context=True)(day_plan)
register.inclusion_tag('diet/meals_section_view.html')(meals_section_view)