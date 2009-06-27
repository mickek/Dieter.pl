from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

@login_required
def settings(request):
    
    form = PasswordChangeForm(request.user)
    
    return render_to_response("patients/settings.html",{'form':form},context_instance=RequestContext(request))