# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from dieter.utils import profile_complete_required, today as get_today, today,\
    no_cache
from dieter.diet.models import Diet
from django.views.generic.simple import direct_to_template, redirect_to
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from dieter.diet.forms import SetDietStartDateForm, CreateDietForm
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage
from dieter.diet import copy_and_activate_diet, get_active_diet, diet_comparator
from dieter import DieterException
import datetime

@login_required
@profile_complete_required
def index(request, year=None, month=None, day=None):
    """
    Diet index may be in three distinct states:
     * there's no diet introduced yet, showing choose diet form
     * there's a diet, but the starting day haven't been choosen
     * there's a diet and the starting day has been choosen  
    """
    try:
        
        today = get_today()
        requested_day = datetime.date(int(year),int(month),int(day)) if ( year or month or day ) else today
        yesterday = requested_day - datetime.timedelta(days=1)
        tommorow = requested_day + datetime.timedelta(days=1)
        
        diet = get_active_diet(request.user)        

        if diet.start_date: # there's a diet and the starting day has been choosen
            
            days = [ diet.current_day_plan(requested_day + datetime.timedelta(days=i)) for i in range(3) ]
            no_diet = not any(days)
            
            return direct_to_template(request, 'diet/index.html', locals())
        else:   # there's a diet, but the starting day haven't been choosen
            
            days = diet.dayplan_set.all()
            return direct_to_template(request, 'diet/view.html', locals())
    
    except Diet.DoesNotExist: #@UndefinedVariable  # there's no diet introduced yet
        return redirect_to(request, reverse('diet_choose_diet'))

@login_required
@profile_complete_required
def choose_diet(request, initial = False):
    
    try:
            
        page_no = int(request.GET['page']) if 'page' in request.GET else 1
        
        user_diets = Diet.objects.filter(user=request.user)
        general_diets = Diet.objects.filter(user__isnull=True).exclude(pk__in = user_diets.values_list('parent_id', flat=True)).order_by('name')
                
        diets = list(user_diets) + list(general_diets)
                
        diets.sort(diet_comparator, reverse = True)
        
        paginator = Paginator(diets,5)
        page = paginator.page(page_no)
        show_pagination = len(paginator.page_range) > 1
        
            
        return direct_to_template(request, 'diet/choose_diet.html', locals())
    except InvalidPage:
        return redirect_to(request, reverse('diet_choose_diet')) 

@login_required
@profile_complete_required
def diet_details(request, diet_id):
    '''
    Ajax loaded
    '''
    diet = get_object_or_404(Diet, pk = diet_id)
    days = diet.dayplan_set.all()
    example_day = min(days)     
    
    return direct_to_template(request, 'diet/details.html', locals())
    
@login_required
@profile_complete_required
def print_diet(request, diet_id=None):

        diet = get_object_or_404(Diet,pk=diet_id) if diet_id else get_object_or_404(Diet,user=request.user, state = 'active')
        days = diet.dayplan_set.all()
        return direct_to_template(request, 'diet/print.html', locals())
    
@login_required
@profile_complete_required
def diet_start_date(request, diet_id):
    
    diet = Diet.objects.get(pk=diet_id)
    form = SetDietStartDateForm(instance=diet)
    
    if request.method == 'POST':
        
        form = SetDietStartDateForm(request.POST, instance=diet)
        if form.is_valid():
            
            if form.cleaned_data['start_date'] is not None:
                request.user.message_set.create(message="Ustalono datę rozpoczęcia diety")
            else:
                request.user.message_set.create(message="Wyłączono dietę")
                
            form.save()
            return HttpResponse('ok', mimetype="application/json")
    
    return direct_to_template(request, 'diet/diet_start_date_form.html', locals())

@login_required
@profile_complete_required
@no_cache
def set_diet(request, diet_id):
    '''
    Ustawia bieżącą dietę użytkownika
    
    Jeśli dieta jest dietą wzorcową to kopiuje ją jako nową dietę przypisaną do wybranego usera
    Jeśli dieta jest wybranego usera to ustawia ją jako active a pozostałe jako inactive
    W przyszłośći tutaj będą realizowane opłaty
    '''
    
    diet = get_object_or_404(Diet, pk=diet_id)
    
    try:
        copy_and_activate_diet(diet, request.user, start_date = today())
        request.user.message_set.create(message="Wybrano dietę oraz ustawiono datę rozpoczęcia na dzisiaj.")
    except DieterException:
        request.user.message_set.create(message="Nie można dwukrotnie wybrać tej samej diety")
    
    return redirect_to(request, reverse('diet'))

@login_required
@profile_complete_required
def create_diet(request):
    form = CreateDietForm()
    
    if request.method == 'POST':
    
        empty_diet = Diet(**{'user':request.user, 'type':'user_created'})
        form = CreateDietForm(request.POST, instance = empty_diet)    
        if form.is_valid():
            
            diet = form.save()
            request.user.message_set.create(message="Utworzono nową dietę do edycji.")
            for i in range(1,form.cleaned_data['diet_length']+1):
                diet.dayplan_set.create(sequence_no=i)
                diet.save()
            
            copy_and_activate_diet(diet, request.user, today())
            
            return redirect(reverse('edit_diet_user'))
    
    
    return direct_to_template(request, "diet/create_diet.html", locals())    