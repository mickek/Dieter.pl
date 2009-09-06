# -*- coding: utf-8 -*-    

from django import template
from dieter.patients.utils import approximate_user_data
import datetime

register = template.Library()

@register.simple_tag
def weight_graph(user, end_day, length):
    
    start_day = end_day - datetime.timedelta(days=length)
    approximated_weight = approximate_user_data(user.userdata_set.filter(date__range=(start_day,end_day)), 'weight', extend_left=30)

    if not approximated_weight: return {'data':None}
    
    data = []
    for i in range(len(approximated_weight)):
        data.append({'weight':approximated_weight[i],'date':start_day+datetime.timedelta(days=i)})
    
    min_val = int(min(approximated_weight)*0.8)
    max_val = int(max(approximated_weight)*1.1)
    
    return {'data':data, 'rows':len(data), 'min':min_val, 'max':max_val}
    
register.inclusion_tag('graphs/weight_graph.html')(weight_graph)