from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.forms import AuthenticationForm

from django.core.urlresolvers import reverse
from django.views.generic.simple import redirect_to

def index(request):
    
    if request.user.is_authenticated():
        return redirect_to(request, reverse('logged_in'))
    
    
    return render_to_response("home/index.html", {'form':AuthenticationForm()}, context_instance=RequestContext(request))

def logged_in(request):
    
    if request.user.is_staff:
        return redirect_to(request, reverse('patients_list'))
    
    if request.user.is_authenticated():
        return redirect_to(request, reverse('dashboard'))
        
