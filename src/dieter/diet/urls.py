from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^edit/(?P<profile_id>[0-9]+)/$','dieter.diet.views.edit', name='edit_diet')    
)