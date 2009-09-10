# -*- coding: utf-8 -*-    

from django import template
from django.utils import simplejson
from dieter.patients import approximate_user_data
import datetime

register = template.Library()

@register.simple_tag
def weight_graph(user, end_day, length, today):
    
    start_day = end_day - datetime.timedelta(days=length)
    
    if today < start_day: 
        length = (end_day - today).days
        start_day = today
    
    approximated_weight = approximate_user_data(user.userdata_set.filter(date__range=(start_day,end_day)), 'weight', extend_left=length)

    if not approximated_weight: return {'data':None}
    modifier = 0
    if len(approximated_weight) == (today - start_day).days: modifier = 1
    
    today_value = approximated_weight[(today - start_day).days - modifier]
    
    data = []
    for i in range(len(approximated_weight)):
        date = start_day+datetime.timedelta(days=i)
        data.append(["%s-%s-%s" % (date.year,date.month,date.day), approximated_weight[i]])

    return {'plot_data':simplejson.dumps(
                                         [data, [["%s-%s-%s"%(today.year,today.month,today.day),today_value]]]
                                         )}
    
register.inclusion_tag('graphs/weight_graph.html')(weight_graph)