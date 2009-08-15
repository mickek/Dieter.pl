from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^create/(?P<user_id>[0-9]+)/$','dieter.diet.views.create', name='create_diet'),                       
    url(r'^edit/(?P<diet_id>[0-9]+)/$','dieter.diet.views.edit', name='edit_diet'),
    url(r'^edit/(?P<diet_id>[0-9]+)/(?P<day>[0-9]+)/$','dieter.diet.views.edit', name='edit_diet'),    
    url(r'^add_day/(?P<diet_id>[0-9]+)/$','dieter.diet.views.add_day', name='diet_add_day'),
    url(r'^add_day/(?P<diet_id>[0-9]+)/(?P<day>[0-9]+)/$','dieter.diet.views.add_day', name='diet_add_day'),
    url(r'^remove_day/(?P<diet_id>[0-9]+)/$','dieter.diet.views.remove_day', name='diet_remove_day'),
    url(r'^remove_day/(?P<diet_id>[0-9]+)/(?P<day>[0-9]+)/$','dieter.diet.views.remove_day', name='diet_remove_day'),    
)