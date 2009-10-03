from django.contrib.auth.decorators import login_required
from dieter.utils import profile_complete_required, DieterException, today as get_today
    
from django.views.generic.simple import direct_to_template, redirect_to
from dieter.dashboard.forms import WeightForm
from django.http import HttpResponse
from dieter.diet.models import Diet
import datetime
from django.core.urlresolvers import reverse

@login_required
@profile_complete_required
def index(request, year=None, month=None, day=None):
    
    try:

        diet = None
        day_plan = None

        today = get_today()
        requested_day = datetime.date(int(year),int(month),int(day)) if ( year or month or day ) else today
        if requested_day > today: raise DieterException("Can't show future")
        
        profile = request.user.get_profile()
        
        try:
            diet = Diet.objects.get(user=request.user)
            day_plan = diet.current_day_plan(requested_day)
        except Diet.DoesNotExist: #@UndefinedVariable
            pass
        
    
        yesterday = requested_day - datetime.timedelta(days=1)
        tommorow = requested_day + datetime.timedelta(days=1) if requested_day < today else None
        
        current_weight = request.user.get_profile().get_user_data(requested_day).weight
        
        diff_weight_1_week = profile.get_diff(today,"weight",1,"week")
        diff_bmi_1_week = profile.get_diff(today,"bmi",1,"week")
        diff_weight_1_month = profile.get_diff(today,"weight",1,"month")
        diff_bmi_1_month = profile.get_diff(today,"bmi",1,"month")
        
        return direct_to_template(request, "dashboard/index.html",
                                  extra_context = locals())
        
    except ValueError:
        return redirect_to(request, reverse('dashboard'))
    except DieterException:
        return redirect_to(request, reverse('dashboard'))


@login_required
def save_weight(request, year=None, month=None, day=None):
    
    try:
        data = request.user.get_profile().get_user_data(datetime.date(int(year),int(month),int(day)))
        data.weight = float(request.REQUEST['weight'])
        data.save()
        return HttpResponse('"ok"', mimetype="application/json")        
    except:
        return HttpResponse('"error"', mimetype="application/json", status=500)
    
    
