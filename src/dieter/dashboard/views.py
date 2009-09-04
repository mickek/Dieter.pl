from django.contrib.auth.decorators import login_required
from dieter.utils import profile_complete_required, DieterException, today as get_today
    
from django.views.generic.simple import direct_to_template, redirect_to
from dieter.dashboard.forms import WeightForm
from django.http import HttpResponse
from dieter.patients.utils import calculate_weight_difference
import datetime
from django.core.urlresolvers import reverse

@login_required
@profile_complete_required
def index(request, year=None, month=None, day=None):
    
    try:
        
        today = get_today()
        week_before = today - datetime.timedelta(days=7)
        
        calculate_weight_difference(week_before, today, request.user)
        
        requested_day = datetime.datetime(int(year),int(month),int(day)) if ( year or month or day ) else today
        if requested_day > today: raise DieterException("Can't show future")

        yesterday = requested_day - datetime.timedelta(days=1)
        tommorow = requested_day + datetime.timedelta(days=1) if requested_day < today else None
        
        weight_form = WeightForm(instance = request.user.get_profile().get_user_data(requested_day))
        
        return direct_to_template(request, "dashboard/index.html",
                                  extra_context = locals())
        
    except ValueError, DieterException:
        return redirect_to(request, reverse('dashboard'))



def save_weight(request, year=None, month=None, day=None):
    
    try:
        data = request.user.get_profile().get_user_data(datetime.datetime(int(year),int(month),int(day)))
        data.weight = float(request.REQUEST['weight'])
        data.save()
        return HttpResponse('"ok"', mimetype="application/json")        
    except:
        return HttpResponse('"error"', mimetype="application/json", status=500)
    
    
