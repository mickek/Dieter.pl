from django.contrib.auth.decorators import login_required
from dieter.utils import profile_complete_required, today as get_today
from django.views.generic.simple import direct_to_template
from dieter.patients.models import UserData

@login_required
@profile_complete_required
def index(request, mode = 'week'):


    today = get_today()
    
    max_length = len(UserData.objects.all())
    
    if mode == 'week':
        graph_length = min(7,max_length)
    elif mode == 'month':
        graph_length = min(31,max_length)
    else:
        graph_length = max_length

    return direct_to_template(request, 'graphs/index.html', locals())
