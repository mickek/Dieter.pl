# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from django.shortcuts import redirect, get_object_or_404
from django.core.urlresolvers import reverse
from dieter.diet.models import Diet, DayPlan
from django.contrib.auth.models import User

@login_required
def create(request, user_id):
    
    diet, created = Diet.objects.get_or_create(user=User.objects.get(pk=user_id))
    if created: request.user.message_set.create(message="Utworzono nową dietę do edycji.")
    return redirect(reverse('edit_diet',kwargs={'diet_id':diet.id}))

@login_required
def edit(request, diet_id, day = None):
    
    diet = get_object_or_404(Diet, pk=diet_id)
    
    try:
        current_day = diet.dayplan_set.get(sequence_no=day)
    except DayPlan.DoesNotExist: #@UndefinedVariable
        current_day = min(diet.dayplan_set.all())
                
    return direct_to_template(request,"diet/edit.html", {
                                                        'diet': diet, 
                                                        'days': diet.dayplan_set.all(),
                                                        'current_day': current_day,
                                                        'can_delete': len(diet.dayplan_set.all())>1,
                                                        'breakfest': current_day.meal_set.filter(type='breakfest'),
                                                        'brunch': current_day.meal_set.filter(type='brunch'),
                                                        'lunch': current_day.meal_set.filter(type='lunch'),
                                                        'dinner': current_day.meal_set.filter(type='dinner'),
                                                        })
    
@login_required
def add_day(request, diet_id, day = None):

    diet = get_object_or_404(Diet, pk=diet_id)
    day = diet.add_day(day)
    
    request.user.message_set.create(message="Dodano dzień")
    return redirect(reverse('edit_diet',kwargs={'diet_id':diet_id, 'day':day}))

@login_required
def del_day(request, diet_id, day = None):
    
    diet = get_object_or_404(Diet, pk=diet_id)    
    status = diet.remove_day(int(day))
    
    if not status:
        request.user.message_set.create(message="Nie można skasować wszystkich dni diety")
        return redirect(reverse('edit_diet',kwargs={'diet_id':diet_id}))        
    
    request.user.message_set.create(message="Usunięto dzień")
    return redirect(reverse('edit_diet',kwargs={'diet_id':diet_id, 'day': status}))

def perform_action(request, diet_id, sequence_no):

    day = get_object_or_404(DayPlan, sequence_no = sequence_no, diet__id = diet_id)
    if request.method == 'POST': 
        
        if 'save_day' in request.POST:
            request.user.message_set.create(message="Zapisano dzień")
            sequence_no = int(sequence_no)
            
            meals = zip( request.POST.getlist('meal_type'), request.POST.getlist('meal_name'), request.POST.getlist('meal_quantity') )
            
            for meal in day.meal_set.all(): meal.delete()
            for i, row in enumerate(meals):
                meal_type, meal_name, meal_quantity = row
                day.meal_set.create( type=meal_type, name=meal_name, quantity=meal_quantity, sequence_no=i )
                
            day.save()
            
            
            
        if 'save_diet' in request.POST:
            request.user.message_set.create(message="Zapisano dietę")
            
        if 'send_diet' in request.POST:
            request.user.message_set.create(message="Wysłano dietę ( TODO )")
            
            

    return redirect(reverse('edit_diet',kwargs={'diet_id':diet_id, 'day': sequence_no}))    
    

def add_meal_debug(request, diet_id, sequence_no):
    
    day = get_object_or_404(DayPlan, sequence_no = sequence_no, diet__id = diet_id)
    print day.meal_set.filter(type = request.POST['type'])
    
    if day.meal_set.filter(type = request.POST['type']):
        meal_sequence_no = max(day.meal_set.filter(type = request.POST['type'])).sequence_no + 1        
    else:
        meal_sequence_no = 1        

        
    day.meal_set.create( type = request.POST['type'], name = request.POST['name'], quantity = request.POST['quantity'], sequence_no = meal_sequence_no )
    day.save()
    
    request.user.message_set.create(message="Dodano posiłek (debug)")
    
    return redirect(reverse('edit_diet',kwargs={'diet_id':diet_id, 'day': sequence_no}))