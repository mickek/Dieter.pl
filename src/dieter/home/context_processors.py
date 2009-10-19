from dieter.diet.models import Diet
from dieter.diet import get_active_diet
def tabs(request):

    top_tab = 'dashboard'

    path = request.path_info

    if path.startswith('/dashboard'):
        top_tab = 'dashboard'
    elif path.startswith('/diet'):
        top_tab = 'diet'
    elif path.startswith('/graphs'):
        top_tab = 'graphs'
    elif path.startswith('/shopping'):
        top_tab = 'shopping'
    elif path.startswith('/inbox') or path.startswith('/comments'):
        top_tab = 'inbox'
    elif path.startswith('/patients/settings') or path.startswith('/accounts/password/change/'):
        top_tab = 'settings'
    elif path.startswith('/managment'):
        top_tab = 'managment'
        
    
    if path.startswith('/patients/inbox'):
        top_tab = 'messages'        
    elif path == '/patients/' or path.startswith('/diet/edit/'):
        top_tab = 'patients'                
    
    user_has_diet = False
    user_diet_started = False
    try:   
        if request.user.is_authenticated(): 
            diet = get_active_diet(request.user)
            user_has_diet = diet is not None
            user_diet_started = diet.start_date is not None
    except Diet.DoesNotExist: #@UndefinedVariable
        pass
        
    
    return {
        'top_tab':top_tab,
        'user_has_diet': user_has_diet,
        'user_diet_started' : user_diet_started
    }
    