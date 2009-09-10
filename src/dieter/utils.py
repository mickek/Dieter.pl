from django.utils.functional import update_wrapper
from django.views.generic.simple import redirect_to
from django.core.urlresolvers import reverse
import re
import datetime

def profile_complete_required(f):
    def wrap(request, *args, **kwargs):
        
        if request.user.get_profile().is_profile_complete():
            return f(request, *args, **kwargs)
        else:
            return redirect_to(request, reverse('complete_profile'))    
    update_wrapper(wrap, f)
    return wrap

def today():
    today = datetime.date.today()
    return datetime.date(today.year, today.month, today.day)

def tommorow():
    return today() + datetime.timedelta(days=1)

def yesterday():
    return today() - datetime.timedelta(days=1)
    
    
class DieterException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)   
        
def calculate_similarity(text1, text2):

    t1 = re.sub(r"[^a-z0-9 ]", '', text1.lower()).split()
    t2 = re.sub(r"[^a-z0-9 ]", '', text2.lower()).split()

    intersection = []

    for l in t1:
        if l in t2: intersection.append(l)

    sum = t1

    for l in t2:
        if l not in t1: sum.append(l)

    coefficient = float(len(intersection)) / float(len(sum))

    return coefficient   
