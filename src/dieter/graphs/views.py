# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from dieter.utils import profile_complete_required, today as get_today
from django.views.generic.simple import direct_to_template
import datetime

MONTH_LENGTH    = 31
WEEK_LENGTH     = 7

@login_required
@profile_complete_required
def index(request, mode = 'week'):

    today = get_today()
    
    if mode == 'week':
        graph_length = WEEK_LENGTH
    elif mode == 'month':
        graph_length = MONTH_LENGTH
    else:
        '''
        Wyświetlamy albo ostatnie 31 dni albo okres od rejestracji do dzisiaj
        '''
        date_joined = request.user.date_joined
        graph_length = (today - datetime.date(date_joined.year, date_joined.month, date_joined.day)).days
        graph_length = max(MONTH_LENGTH, graph_length)

    return direct_to_template(request, 'graphs/index.html', locals())
