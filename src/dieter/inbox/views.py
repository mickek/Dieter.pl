from django.views.generic.simple import direct_to_template
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: 'patient' in u.groups.values_list('name',flat=True), login_url='/dashboard/')
def index(request):
    
    return direct_to_template(request, 'inbox/index.html', extra_context = {
                                                                            'comment_redirect' :reverse('inbox'),
                                                                            })