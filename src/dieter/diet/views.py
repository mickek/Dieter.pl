# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from django.shortcuts import redirect, get_object_or_404
from django.core.urlresolvers import reverse
from dieter.diet.models import Diet, DayPlan, Food, Meal
from django.contrib.auth.models import User
from api import parse_quantity
from django.http import HttpResponse, HttpResponseNotFound
from dieter.utils import DieterException, profile_complete_required, today as get_today
from dieter.diet.forms import SetDietStartDateForm
import datetime

@login_required
@profile_complete_required
def index(request, year=None, month=None, day=None):
    """
    Diet index may be in three distinct states:
     * there's no diet introduced yet
     * there's a diet, but the starting day haven't been choosen
     * there's a diet and the starting day has been choosen  
    """
    try:
        
        today = get_today()
        requested_day = datetime.date(int(year),int(month),int(day)) if ( year or month or day ) else today
        yesterday = requested_day - datetime.timedelta(days=1)
        tommorow = requested_day + datetime.timedelta(days=1)
        
        diet = Diet.objects.get(user=request.user)        

        if diet.start_date: # there's a diet and the starting day has been choosen
            
            days = [ diet.current_day_plan(requested_day + datetime.timedelta(days=i)) for i in range(3) ]
            print days
            no_diet = not any(days)
            
            return direct_to_template(request, 'diet/index.html', locals())
        else:   # there's a diet, but the starting day haven't been choosen
            
            days = diet.dayplan_set.all()
            return direct_to_template(request, 'diet/view.html', locals())
    
    except Diet.DoesNotExist: #@UndefinedVariable  # there's no diet introduced yet
        return direct_to_template(request, 'diet/no-diet-yet.html')
    
@login_required
@profile_complete_required
def print_diet(request, diet_id=None):
    
    try:
        diet = Diet.objects.get(pk=diet_id) if diet_id else Diet.objects.get(user=request.user)
        days = diet.dayplan_set.all()
        return direct_to_template(request, 'diet/print.html', locals())
    except Diet.DoesNotExist: #@UndefinedVariable
        return HttpResponseNotFound('<h1>Nie znaleziono diety</h1>')
    
@login_required
def diet_start_date(request, diet_id):
    
    diet = Diet.objects.get(pk=diet_id)
    form = SetDietStartDateForm(instance=diet)
    
    if request.method == 'POST':
        
        form = SetDietStartDateForm(request.POST, instance=diet)
        if form.is_valid():
            request.user.message_set.create(message="Ustalono datę rozpoczęcia diety")
            form.save()
            return HttpResponse('ok', mimetype="application/json")
    
    return direct_to_template(request, 'diet/diet_start_date_form.html', locals())

@login_required
def create(request, user_id):
    """
    Creates a new diet for a given user.
    If diet already exists just redirects to edit screen 
    """
    
    diet, created = Diet.objects.get_or_create(user=User.objects.get(pk=user_id))
    if created: request.user.message_set.create(message="Utworzono nową dietę do edycji.")
    return redirect(reverse('edit_diet',kwargs={'diet_id':diet.id}))

@login_required
def edit(request, diet_id, day = None):
    """
    Diet edit screen
    """
    
    diet = get_object_or_404(Diet, pk=diet_id)
    
    try:
        current_day = diet.dayplan_set.get(sequence_no=day)
    except DayPlan.DoesNotExist: #@UndefinedVariable
        current_day = min(diet.dayplan_set.all())
                
    return direct_to_template(request,"diet/edit.html", {
                                                        'diet': diet, 
                                                        'days': diet.dayplan_set.all(),
                                                        'current_day': current_day,
                                                        'can_delete': len(diet.dayplan_set.all())>1
                                                        })
    
@login_required
def add_day(request, diet_id, day = None):
    """
    Adds a new day to selected diet and redirects to edit screen for the new day
    """

    diet = get_object_or_404(Diet, pk=diet_id)
    day = diet.add_day(day)
    
    request.user.message_set.create(message="Dodano dzień")
    return redirect(reverse('edit_diet',kwargs={'diet_id':diet_id, 'day':day}))

@login_required
def del_day(request, diet_id, day = None):
    """
    Removes a day from selected diet and redirects to previous day
    """
    status = None
    try:
        diet = get_object_or_404(Diet, pk=diet_id)    
        status = diet.remove_day(int(day))
        request.user.message_set.create(message="Usunięto dzień")
        
    except DieterException:
        request.user.message_set.create(message="Nie można skasować wszystkich dni diety")
        
    return redirect(reverse('edit_diet',kwargs={'diet_id':diet_id, 'day': status}))                
        

@login_required
def perform_action(request, diet_id, sequence_no):
    """
    Bulk action handler for diet editing, handlers for save and send diet
    """

    day = get_object_or_404(DayPlan, sequence_no = sequence_no, diet__id = diet_id)
    if request.method == 'POST': 
        
        if 'save_day' or 'save_diet' in request.POST:
            sequence_no = int(sequence_no)+1
            
            meals = zip( request.POST.getlist('meal_type'), request.POST.getlist('meal_name'), request.POST.getlist('meal_quantity') )

            for meal in day.meal_set.all(): meal.delete()
            for i, row in enumerate(meals):

                meal_type, meal_name, meal_quantity = row
                quantity, unit_type = parse_quantity(meal_quantity)
                
                if meal_name != '' and meal_type in ['breakfest','brunch','lunch','dinner']:
                    day.meal_set.create( type=meal_type, name=meal_name, quantity=quantity, unit_type = unit_type, sequence_no=i )
                
            day.save()
            
        if 'save_day' in request.POST:
            request.user.message_set.create(message="Zapisano dzień")
            
        if 'save_diet' in request.POST:
            request.user.message_set.create(message="Zapisano dietę")
            
        if 'send_diet' in request.POST:
            request.user.message_set.create(message="Wysłano dietę ( TODO )")
            
    return redirect(reverse('edit_diet',kwargs={'diet_id':diet_id, 'day': sequence_no}))    
    
def food_autocomplete(request):
    """
    Autocompletes for food returns items separated by new line
    """
    
    items = []
    q = request.GET['q']
    limit = int(request.GET['limit']) 
    
    items.extend(Food.objects.filter(name__icontains = q).values_list('name',flat=True))
    items.extend(Meal.objects.filter(name__icontains = q).values_list('name',flat=True))
    items = [ item.lower() for item in items ]
    
    distinct_items = set(items)
    
    items = []
    items.extend(distinct_items)
    items.sort()

    return HttpResponse("\n".join(items[:limit]))