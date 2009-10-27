# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic.simple import direct_to_template
from django.shortcuts import redirect, get_object_or_404
from django.core.urlresolvers import reverse
from dieter.diet.models import Diet, DayPlan, Food, Meal
from django.contrib.auth.models import User
from dieter.diet.forms import SendDietForm
from django.contrib.comments.models import Comment
from django.conf import settings
from dieter.utils import diet_read_write_allowed
from dieter.diet import parse_quantity, get_active_diet, data_for_diet_editing
from django.http import HttpResponse
from dieter import DieterException
import datetime

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/')
def create(request, user_id):
    """
    Creates a new diet for a given user.
    If diet already exists just redirects to edit screen 
    """
    
    diet, created = Diet.objects.get_or_create(user=User.objects.get(pk=user_id), type='nutronist_created')
    if created: request.user.message_set.create(message="Utworzono nową dietę do edycji.")
    return redirect(reverse('edit_diet',kwargs={'diet_id':diet.id}))

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/')
def edit_for_admin(request, diet_id = None, day = None):
    """
    Diet edit screen
    """
    diet = get_object_or_404(Diet, pk=diet_id)
    current_day, days, can_delete = data_for_diet_editing(diet, day)
    type = "edit_diet"
                    
    return direct_to_template(request,"diet/edit.html", locals())

@login_required
def edit_for_user(request, day = None):
    """
    Diet edit screen
    """
    diet = get_active_diet(request.user)
    
    if diet.type != 'user_created' is not None:
        request.user.message_set.create(message="Nie możesz edytować diety utworzonej przez kogoś innego")
        return redirect(reverse('diet')) 
    
    current_day, days, can_delete = data_for_diet_editing(diet, day)
    type = "edit_diet_user"    
    
    return direct_to_template(request,"diet/user_edit.html", locals())
    
@login_required
@diet_read_write_allowed
def add_day(request, diet_id, day = None):
    """
    Adds a new day to selected diet and redirects to edit screen for the new day
    """
    diet = get_object_or_404(Diet, pk=diet_id)
    day = diet.add_day(day)
    request.user.message_set.create(message="Dodano dzień")
    
    if request.user.is_staff:    
        return redirect(reverse('edit_diet',kwargs={'diet_id':diet_id, 'day': day}))
    else:                
        return redirect(reverse('edit_diet_user',kwargs={'day': day}))


@login_required
@diet_read_write_allowed
def del_day(request, diet_id, day = None):
    """
    Removes a day from selected diet and redirects to previous day
    """
    sequence_no = None
    try:
        diet = get_object_or_404(Diet, pk=diet_id)    
        sequence_no = diet.remove_day(int(day))
        request.user.message_set.create(message="Usunięto dzień")
        
    except DieterException:
        request.user.message_set.create(message="Nie można skasować wszystkich dni diety")
        
    if request.user.is_staff:    
        return redirect(reverse('edit_diet',kwargs={'diet_id':diet_id, 'day': sequence_no}))
    else:                
        return redirect(reverse('edit_diet_user',kwargs={'day': sequence_no}))
        

@login_required
@diet_read_write_allowed
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
            return redirect('/')
            
        if 'send_diet' in request.POST:
            return redirect(reverse('diet_send_form',kwargs={'diet_id':diet_id}))
            
    if request.user.is_staff:    
        return redirect(reverse('edit_diet',kwargs={'diet_id':diet_id, 'day': sequence_no}))
    else:                
        return redirect(reverse('edit_diet_user',kwargs={'day': sequence_no}))

@user_passes_test(lambda u: u.is_staff, login_url='/')
def send_diet(request, diet_id):
    
    diet = get_object_or_404(Diet, pk = diet_id)
    form = SendDietForm(request.POST)
    if request.method == 'POST' and form.is_valid():
        comment = Comment( content_object= diet.user,
                           user_name    = request.user.username,
                           user_email   = request.user.email,
                           comment      = form.cleaned_data["message"],
                           submit_date  = datetime.datetime.now(),
                           site_id      = settings.SITE_ID,
                           is_public    = True,
                           is_removed   = False,
                          )
        comment.save()
        diet.state='sent'
        diet.save()
        
        request.user.message_set.create(message="Zapisano dietę i wysłano wiadomość do pacjenta")
        
        return redirect(reverse('patients_list'))

    return direct_to_template(request, 'diet/send_diet.html', locals())
    
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