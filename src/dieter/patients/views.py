from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic.simple import direct_to_template, redirect_to
from dieter.patients.models import Profile
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from dieter.patients.forms import ProfileSettingsForm


@login_required
def settings(request):
    
    password_form = PasswordChangeForm(request.user)
    profile_form = ProfileSettingsForm(instance=request.user.get_profile())
    return direct_to_template(request, "patients/settings.html", extra_context=locals())

def save_settings(request):
    
    if request.method == 'POST':

        password_form = PasswordChangeForm(request.user)
        profile_form = ProfileSettingsForm(request.POST, instance = request.user.get_profile())
        if profile_form.is_valid():
            request.user.message_set.create(message="Zapisano dane profilu")
            profile_form.save()
            
        return direct_to_template(request, "patients/settings.html", extra_context=locals())
        
    else: return redirect_to(request, reverse('settings'))
    
    
    

@login_required
def patients_list(request):
    
    patients = Profile.objects.filter(user__is_staff=False, user__is_active=True, user__is_superuser=False)
    return direct_to_template(request, "patients/patients_list.html", {'patients':patients})

@login_required
def patients_inbox(request, user_id):
    
    owner = get_object_or_404(User, pk=user_id)
    comment_redirect = reverse('patients_inbox',args=(user_id,))
    return direct_to_template(request, "patients/patients_inbox.html", extra_context=locals())