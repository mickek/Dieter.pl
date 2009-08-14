from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^settings/$','dieter.patients.views.settings', name='settings'),
    url(r'^$','dieter.patients.views.patients_list', name='patients_list')    
)