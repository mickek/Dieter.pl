# Create your views here.
from django.contrib.auth.decorators import login_required, user_passes_test
from dieter.patients.models import Profile
from django.views.generic.simple import direct_to_template

@user_passes_test(lambda u: u.is_superuser, login_url='/dashboard/')
def index(request):
    
    return direct_to_template(request, "managment/index.html", locals())