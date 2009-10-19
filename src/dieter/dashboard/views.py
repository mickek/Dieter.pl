from django.contrib.auth.decorators import login_required, user_passes_test
from dieter.utils import profile_complete_required, DieterException, today as get_today
    
from django.views.generic.simple import direct_to_template, redirect_to
from django.http import HttpResponse
from dieter.diet.models import Diet
from dieter.diet import get_active_diet
import datetime
from django.core.urlresolvers import reverse

@login_required
@user_passes_test(lambda u: not u.is_superuser and not u.is_staff, login_url='/')
@profile_complete_required
def index(request, year=None, month=None, day=None):
    
    try:
        
        '''
        A bit of hack, no idea how to do it better now
        '''
        if 'choose_diet' in request.session:
            return redirect_to(request, reverse('diet_choose_diet'))    

        diet = None
        day_plan = None

        today = get_today()
        requested_day = datetime.date(int(year),int(month),int(day)) if ( year or month or day ) else today
        if requested_day > today: raise DieterException("Can't show future")
        
        profile = request.user.get_profile()
        
        try:
            diet = get_active_diet(request.user)
            day_plan = diet.current_day_plan(requested_day)
            if diet.end_day():
                days_left = (diet.end_day() - today).days
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
    
    
