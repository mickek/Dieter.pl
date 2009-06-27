from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^settings/$','dieter.patients.views.settings', name='settings')    
)