from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic.simple import direct_to_template
from dieter.patients.models import Profile
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


@login_required
def settings(request):
    
    form = PasswordChangeForm(request.user)
    return direct_to_template(request, "patients/settings.html", extra_context={'form':form})

@login_required
def patients_list(request):
    
    patients = Profile.objects.filter(user__is_staff=False, user__is_active=True, user__is_superuser=False)
    return direct_to_template(request, "patients/patients_list.html", {'patients':patients})

@login_required
def patients_inbox(request, user_id):
    
    owner = get_object_or_404(User, pk=user_id)
    comment_redirect = reverse('patients_inbox',args=(user_id,))
    return direct_to_template(request, "patients/patients_inbox.html", extra_context=locals())