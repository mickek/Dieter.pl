from django.contrib.auth.decorators import login_required
from dieter.utils import profile_complete_required, today as get_today
from django.views.generic.simple import direct_to_template
import datetime

@login_required
@profile_complete_required
def index(request, mode = 'week'):
    
    if mode == 'week':
        graph_length = 7
    elif mode == 'month':
        graph_length = 31
    else:
        date_joined = request.user.date_joined
        graph_length = (today - datetime.date(date_joined.year, date_joined.month, date_joined.day)).days
        graph_length = max(31, graph_length)

    return direct_to_template(request, 'graphs/index.html', locals())
