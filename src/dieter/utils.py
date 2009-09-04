from django.utils.functional import update_wrapper
from django.views.generic.simple import redirect_to
from django.core.urlresolvers import reverse
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
    return datetime.date(today.year, today.month,today.day)

def tommorow():
    return today() + datetime.timedelta(days=1)

def yesterday():
    return today() - datetime.timedelta(days=1)
    
    
class DieterException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)    