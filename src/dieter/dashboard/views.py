from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from dieter.utils import profile_complete_required

@login_required
@profile_complete_required
def index(request):
    
    return render_to_response("dashboard/index.html", {}, context_instance=RequestContext(request))    
