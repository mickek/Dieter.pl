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

def today_tommrow():
    
    today = datetime.datetime.today()
    
    today = datetime.datetime(today.year, today.month,today.day)
    tommorow = today + datetime.timedelta(days=1)
    
    return (today,tommorow,)    
    