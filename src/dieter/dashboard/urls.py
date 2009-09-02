from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$','dieter.dashboard.views.index', name='dashboard'),
    url(r'^save_weight/$', 'dieter.dashboard.views.save_weight', name='dashboard_save_weight')    
)