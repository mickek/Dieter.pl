from django.utils.functional import update_wrapper
from django.views.generic.simple import redirect_to
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from dieter.diet.models import Diet
from dieter.diet import get_active_diet

import re
import datetime

def has_read_write_access_to_diet(user, diet):
    
    if user.is_superuser:
        return True
    
    if diet.user == user:
        return True
    
    if user.is_staff and user.practice:
        '''
        TODO private practice staff may edit someone else diet
        '''
        pass
        
    return False

def profile_complete_required(f):
    def wrap(request, *args, **kwargs):
        
        if request.user.get_profile().is_profile_complete():
            return f(request, *args, **kwargs)
        else:
            return redirect_to(request, reverse('complete_profile'))

    update_wrapper(wrap, f)
    return wrap

def diet_read_write_allowed(f):
    def wrap(request, *args, **kwargs):
        diet = None
        try:
            if 'diet_id' in request.REQUEST:
                diet = Diet.objects.get(pk=request.REQUEST['diet_id'])
            else:
                diet = get_active_diet(request.user)
            if has_read_write_access_to_diet(request.user, diet):
                return f(request, *args, **kwargs)
            else:
                return HttpResponseForbidden(content='Forbiden')
        except Diet.DoesNotExist: #@UndefinedVariable
            return f(request, *args, **kwargs)
    update_wrapper(wrap, f)
    return wrap

def no_cache(f):
    def wrap(request, *args, **kwargs):
        
        response = f(request, *args, **kwargs)
        response['Pragma'] = 'no-cache'
        return response

    update_wrapper(wrap, f)
    return wrap


def choose_diet_shown_required(f):
    def wrap(request, *args, **kwargs):
        if not 'choose_diet' in request.session:
            return f(request, *args, **kwargs)
        else:
            return redirect_to(request, reverse('diet_choose_diet'))    
    update_wrapper(wrap, f)
    return wrap


def today():
    today = datetime.date.today()
    return datetime.date(today.year, today.month, today.day)

def tommorow():
    return today() + datetime.timedelta(days=1)

def yesterday():
    return today() - datetime.timedelta(days=1)
    
        
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
