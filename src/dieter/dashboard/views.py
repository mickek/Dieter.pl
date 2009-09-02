from django.contrib.auth.decorators import login_required
from dieter.utils import profile_complete_required
from django.views.generic.simple import direct_to_template
from dieter.dashboard.forms import WeightForm
from django.http import HttpResponse

@login_required
@profile_complete_required
def index(request):
    
    p = request.user.get_profile()
    form = WeightForm(instance = p.get_current_data())
    
    return direct_to_template(request, "dashboard/index.html",
                              extra_context = {'weight_form':form})
    
def save_weight(request, day=None):
    
    p = request.user.get_profile()
    data = p.get_current_data()
    data.weight = float(request.POST['weight'])
    data.save()
    
    return HttpResponse('"ok"', mimetype="application/json")    
