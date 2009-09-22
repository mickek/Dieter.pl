from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^settings/$','dieter.patients.views.settings', name='settings'),
    url(r'^$','dieter.patients.views.patients_list', name='patients_list'),
    url(r'^inbox/([0-9]+)/$','dieter.patients.views.patients_inbox', name='patients_inbox'),
    url(r'^save_settings/$','dieter.patients.views.save_settings', name='patients_save_settings')    
)