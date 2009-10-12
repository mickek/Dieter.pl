from dieter.utils import DieterException
from dieter.diet.models import Diet
import re

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

def copy_and_activate_diet(source_diet, target_user):
    '''
    Check if target_user has already this diet if he has fail
    Check if target_user has an active diet, deactivate it 
    Copy source_diet to target_user
    Activate new diet
    '''

    current_diet = None
    try:    # checking if target_user has already this diet
        current_diet = Diet.objects.get(user=target_user, state = 'active')
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
    