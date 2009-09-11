from django.views.generic.simple import direct_to_template
from django.core.urlresolvers import reverse

# Create your views here.
def index(request):
    
    
    return direct_to_template(request, 'inbox/index.html', extra_context = {
                                                                            'comment_redirect' :reverse('inbox'),
                                                                            })