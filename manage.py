#!/usr/bin/env python

if __name__ == "__main__":
    import os
    import sys
    
    my_path = os.path.dirname(os.path.abspath(__file__))
    
    #Set up PYTHONPATH
    sys.path = [os.path.join(my_path, "libs"),
                os.path.join(my_path, "src")] + sys.path
    
    while my_path in sys.path:
        sys.path.remove(my_path)
    
    #Set up the DJANGO_SETTINGS_MODULE
    from django.conf import ENVIRONMENT_VARIABLE
    
    settings_path = os.path.join(my_path, ENVIRONMENT_VARIABLE)
    
    if not os.path.isfile(settings_path):
        raise Exception("%s file is missing, fill it with the name of the desired settings module, for example: 'project.settings.production'" % ENVIRONMENT_VARIABLE)
    
    os.environ[ENVIRONMENT_VARIABLE] = open(settings_path).read()
    
    #Import settings
    try:
        __mod = __import__(os.environ[ENVIRONMENT_VARIABLE], {}, {}, [''])
    except ImportError, e:
        raise ImportError, "Could not import settings '%s' (Is it on sys.path? Does it have syntax errors?): %s" % (os.environ[ENVIRONMENT_VARIABLE], e)
    
    from django.core.management import execute_manager
    execute_manager(__mod)