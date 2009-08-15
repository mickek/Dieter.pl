from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from django.shortcuts import redirect, get_object_or_404
from django.core.urlresolvers import reverse
from dieter.diet.models import Diet
from django.contrib.auth.models import User

@login_required
def create(request, user_id, length=20):
    
    if len(Diet.objects.filter(user__id=user_id))==0:
        new_diet = Diet.objects.create(user=User.objects.get(pk=user_id))
        for i in range(1,length):
            new_diet.dayplan_set.create(sequence_no=i)
    
        new_diet.save()
    
    return redirect(reverse('edit_diet',kwargs={'diet_id':new_diet.id}))

@login_required
def edit(request, diet_id, day = None):
    
    diet = get_object_or_404(Diet, pk=diet_id)
    return direct_to_template(request,"diet/edit.html", {
                                                        'diet':diet, 
                                                        'days':diet.dayplan_set.all()
                                                        })
    
@login_required
def add_day(request, diet_id, day = None):

    diet = get_object_or_404(Diet, pk=diet_id)

    """
    Always inserting in the end
    """
     
    if day is None:
        """
        We are adding at the end or at the begging
        """
        max_day = max(diet.dayplan_set.all())
        if max_day is None: day = 0
        else: day = max_day.sequence_no+1
    else:
        raise "Adding days in between not Implemented"

    diet.dayplan_set.create(sequence_no=day)
    diet.save()
    """
    Insert day
    """
    return redirect(reverse('edit_diet',kwargs={'diet_id':diet_id}))
    

@login_required
def remove_day(request, diet_id, day = None):
    
    """
    Remove day
    """
    
    """
    Cleanup
    """
    
    return redirect(reverse('edit_diet',kwargs={'diet_id':diet_id}))
