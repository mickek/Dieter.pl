# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.forms import AuthenticationForm

from django.core.urlresolvers import reverse
from django.views.generic.simple import redirect_to, direct_to_template
from dieter.patients.forms import ProfileForm
from django.contrib.auth.decorators import login_required

def index(request):
    
    if request.user.is_authenticated():
        return redirect_to(request, reverse('logged_in'))
        
    return render_to_response("home/index.html", {'form':AuthenticationForm()}, context_instance=RequestContext(request))

def logged_in(request):
    
    if request.user.is_staff:
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

    form = ProfileForm(instance = p)
    if request.method == 'POST':
    
        form = ProfileForm(request.POST, instance=p)
        if form.is_valid():
            
            request.user.userdata_set.create(
                                             weight=form.cleaned_data['current_weight'], 
                                             waist=form.cleaned_data['current_waist'])
            form.save()
            request.user.save()
            
            request.user.message_set.create(message="Uzupełniono profil")
            return redirect_to(request, reverse('dashboard'))
    
    return direct_to_template(request, "home/complete_profile.html", extra_context= {'form':form })