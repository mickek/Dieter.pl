# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.forms import AuthenticationForm

from django.core.urlresolvers import reverse
from django.views.generic.simple import redirect_to, direct_to_template
from dieter.patients.forms import CompleteProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.flatpages.models import FlatPage


def index(request):
    
    if request.user.is_authenticated():
        return redirect_to(request, reverse('logged_in'))
        
    return render_to_response("home/index.html", {'form':AuthenticationForm()}, context_instance=RequestContext(request))

def logged_in(request):
    '''
    Po zalogowaniu nastąpi przekierowanie dla:
     * root'a do panelu managment
     * dietetyka dla panelu pacjentów ( zmienić na nutritionist )
     * zwykłego użytkownika do dashboardu
    '''
    
    if request.user.is_superuser:
        return redirect_to(request, reverse('managment_index'))
    
    if 'nutritionist' in request.user.groups.values_list('name',flat=True):
        return redirect_to(request, reverse('patients_list'))
    
    if request.user.is_authenticated():
        p = request.user.get_profile()
        if p.is_profile_complete():
            return redirect_to(request, reverse('dashboard'))
        else:
            return redirect_to(request, reverse('complete_profile'))

@login_required     
def complete_profile(request):

    p = request.user.get_profile()
    if p.is_profile_complete(): return redirect_to(request, reverse('dashboard'))

    form = CompleteProfileForm(instance = p)
    if request.method == 'POST':
    
        form = CompleteProfileForm(request.POST, instance=p)
        if form.is_valid():
            
            request.user.userdata_set.create(
                                             weight=form.cleaned_data['current_weight'], 
                                             waist=form.cleaned_data['current_waist'])
            form.save()
            request.user.save()
            
            request.user.message_set.create(message="Uzupełniono profil")
            
            try:
                FlatPage.objects.get(url='/wprowadzenie/')
                return redirect_to(request, '/wprowadzenie/')
            except FlatPage.DoesNotExist: #@UndefinedVariable
                return redirect_to(reverse('dashboard'), '/wprowadzenie/')
            

    
    return direct_to_template(request, "home/complete_profile.html", extra_context= {'form':form })