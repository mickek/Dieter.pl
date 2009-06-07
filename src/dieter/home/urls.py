from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$','dieter.home.views.index', name='index')    
)