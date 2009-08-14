from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template

@login_required
def edit(request, profile_id):
    
    return direct_to_template(request,"diet/edit.html")
