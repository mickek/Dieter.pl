from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$','dieter.dashboard.views.index', name='dashboard')    
)