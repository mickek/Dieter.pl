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
    
    if day is None: 
        current_day = min(diet.dayplan_set.all())
    else:
        current_day = diet.dayplan_set.get(sequence_no=day)
                
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
    diet.add_day(day)
    
    request.user.message_set.create(message="Dodano dzień")
    return redirect(reverse('edit_diet',kwargs={'diet_id':diet_id}))

@login_required
def del_day(request, diet_id, day = None):
    
    diet = get_object_or_404(Diet, pk=diet_id)    
    status = diet.remove_day(int(day))
    
    if not status:
        request.user.message_set.create(message="Nie można skasować wszystkich dni diety")
        return redirect(reverse('edit_diet',kwargs={'diet_id':diet_id}))        
    
    request.user.message_set.create(message="Usunięto dzień")
    return redirect(reverse('edit_diet',kwargs={'diet_id':diet_id, 'day': status}))

def add_meal_debug(request, diet_id, sequence_no):
    
    day = get_object_or_404(DayPlan, sequence_no = sequence_no, diet__id = diet_id)
    if len(day.meal_set.filter(type = request.POST['type'])) > 0:
        meal_sequence_no = max(day.meal_set.filter(type = request.POST['type'])).sequence_no + 1
    else:
        meal_sequence_no = 1
        
    day.meal_set.create( type = request.POST['type'], name = request.POST['name'], quantity = request.POST['quantity'], sequence_no = meal_sequence_no )
    day.save()
    
    request.user.message_set.create(message="Dodano posiłek (debug)")
    
    return redirect(reverse('edit_diet',kwargs={'diet_id':diet_id, 'day': sequence_no}))