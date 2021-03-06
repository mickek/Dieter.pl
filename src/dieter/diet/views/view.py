# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from dieter.utils import profile_complete_required, today as get_today
from dieter.diet.models import Diet
from django.views.generic.simple import direct_to_template
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
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

        diet = get_object_or_404(Diet,pk=diet_id) if diet_id else get_object_or_404(Diet,user=request.user)
        days = diet.dayplan_set.all()
        return direct_to_template(request, 'diet/print.html', locals())
    
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