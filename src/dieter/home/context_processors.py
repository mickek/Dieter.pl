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
    elif path.startswith('/contact'):
        top_tab = 'contact'
    elif path.startswith('/patients/settings') or path.startswith('/accounts/password/change/'):
        top_tab = 'settings'
        
    return {
        'top_tab':top_tab,
    }
    