# -*- coding: utf-8 -*-    

from django import template
from dieter.patients.utils import approximate_user_data
from django.utils import simplejson
import datetime

register = template.Library()

@register.simple_tag
def weight_graph(user, end_day, length, today):
    
    start_day = end_day - datetime.timedelta(days=length)
    approximated_weight = approximate_user_data(user.userdata_set.filter(date__range=(start_day,end_day)), 'weight', extend_left=length)

    if not approximated_weight: return {'data':None}
    
    today_value = approximated_weight[(today - start_day).days-1]
    
    data = []
    for i in range(len(approximated_weight)):
        date = start_day+datetime.timedelta(days=i+1)
        data.append(["%s-%s-%s" % (date.year,date.month,date.day), approximated_weight[i]])

    return {'plot_data':simplejson.dumps(
                                         [data, [["%s-%s-%s"%(today.year,today.month,today.day),today_value]]]
                                         )}
    
register.inclusion_tag('graphs/weight_graph.html')(weight_graph)