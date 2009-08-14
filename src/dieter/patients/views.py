from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic.simple import direct_to_template
from dieter.patients.models import Profile


@login_required
def settings(request):
    
    form = PasswordChangeForm(request.user)
    return render_to_response("patients/settings.html",{'form':form},context_instance=RequestContext(request))

@login_required
def patients_list(request):
    
    patients = Profile.objects.filter(user__is_staff=False, user__is_active=True, user__is_superuser=False)
    return direct_to_template(request, "patients/patients_list.html", {'patients':patients})