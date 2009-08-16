# -*- coding: utf-8 -*-   

from django.conf import settings
from registration.models import RegistrationProfile
from django.template.context import RequestContext
from django.contrib.auth import login
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.views.generic.simple import redirect_to

"""
Activates account and authomaticly registers user
"""
def activate(request, activation_key):

    activation_key = activation_key.lower() # Normalize before trying anything with it.
    account = RegistrationProfile.objects.activate_user(activation_key)
    if account:
        """
        small hack so that auto login will work
        """
        account.backend = settings.AUTHENTICATION_BACKENDS[0]
        login(request, account)
        request.user.message_set.create(message="Twoje konto zostało aktywowane, dziękujemy za rejestrację.")
        return redirect_to(request,reverse('dashboard'))
    else:
        return render_to_response('registration/activate.html',
                                  { 'account': account,
                                    'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS },
                                  context_instance=RequestContext(request))