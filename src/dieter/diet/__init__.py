from dieter.utils import DieterException
from dieter.diet.models import Diet, DayPlan
import re

def get_active_diet(user):
    return Diet.objects.get(user=user, state='active')

def data_for_diet_editing(diet, day):
    
    if not len(diet.dayplan_set.all()):
        diet.dayplan_set.create(sequence_no=1)
        diet.save()
    
    current_day = None
    try:
        current_day = diet.dayplan_set.get(sequence_no=day)
    except DayPlan.DoesNotExist: #@UndefinedVariable
        current_day = min(diet.dayplan_set.all())
        
    days = diet.dayplan_set.all()
    can_delete = len(diet.dayplan_set.all()) > 1
    
    return (current_day, days, can_delete,)
    

def parse_quantity(value):
    
    pattern = re.compile(r"([0-9\.,]+)\s*(.*)")
    results = re.search(pattern, value)
    
    if not results: return None, None
    
    quantity, unit_type = float(results.group(1).strip()), results.group(2).strip()
    
    unit_types = {
        "g":          ["g", "gram"],
        "kg":         ["kilogram", "kilo", "kg"],
        "ml":         ["ml"],
        "l":          ["l","litr"],
    }

    for type, values in unit_types.items():
        if unit_type in values: return quantity, type 
    
    if unit_type == '': unit_type = None
    
    return quantity, unit_type

def copy_and_activate_diet(source_diet, target_user, start_date = None):
    '''
    Check if target_user has already this diet if he has fail
    Check if target_user has an active diet, deactivate it 
    Copy source_diet to target_user
    Activate new diet
    '''

    current_diet = None
    try:    # checking if target_user has already this diet
        current_diet = get_active_diet(target_user)
        if current_diet.parent and current_diet.parent.pk == source_diet.pk:
            raise DieterException('can not activate the same diet twice')
    except Diet.DoesNotExist: #@UndefinedVariable
        pass
    
    if current_diet:
        current_diet.state = 'inactive'
        current_diet.save()
    
    new_diet = Diet.objects.create(
                                          user = target_user, 
                                          state = 'active', 
                                          length = len(source_diet.dayplan_set.all())+1, 
                                          name = source_diet.name,
                                          description = source_diet.description,
                                          type = source_diet.type,
                                          price = source_diet.price,
                                          parent = source_diet,
                                          start_date = start_date,
                                          )
    
    for dayplan in source_diet.dayplan_set.all():
        
        new_dayplan = new_diet.dayplan_set.get(sequence_no = dayplan.sequence_no)
        for meal in dayplan.meal_set.all():
            new_dayplan.meal_set.create(
                                        name = meal.name,
                                        type = meal.type,
                                        quantity = meal.quantity,
                                        unit_type = meal.unit_type,
                                        sequence_no = meal.sequence_no)
            
        new_dayplan.save()
        
    return new_diet
    