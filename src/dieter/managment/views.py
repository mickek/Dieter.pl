# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import user_passes_test
from django.views.generic.simple import direct_to_template
from dieter.diet.models import Diet
from dieter.managment.forms import CreateDietForm
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

@user_passes_test(lambda u: u.is_superuser, login_url='/dashboard/')
def index(request):
    
    diets = Diet.objects.filter(user__isnull=True)
    
    return direct_to_template(request, "managment/index.html", locals())

@user_passes_test(lambda u: u.is_superuser, login_url='/dashboard/')
def create_diet(request):
    
    form = CreateDietForm()
    
    if request.method == 'POST':
    
        form = CreateDietForm(request.POST)    
        if form.is_valid():
            
            diet = form.save()
            request.user.message_set.create(message="Utworzono nową dietę do edycji.")
            for i in range(1,form.cleaned_data['diet_length']+1):
                diet.dayplan_set.create(sequence_no=i)
                diet.save()
            return redirect(reverse('edit_diet',kwargs={'diet_id':diet.id}))
    
    
    return direct_to_template(request, "managment/create_diet.html", locals())

def delete_diet(request, diet_id):
    
    try:
        
        diet = Diet.objects.get(pk=diet_id)
        for child in Diet.objects.filter(parent=diet).all():
            child.parent = None
            child.save()
            
        diet.delete()
        request.user.message_set.create(message="Usunięto dietę")
    except Diet.DoesNotExist: #@UndefinedVariable
        request.user.message_set.create(message="Nie znaleziono żądanej diety")
    
    return redirect(reverse('managment_index'))