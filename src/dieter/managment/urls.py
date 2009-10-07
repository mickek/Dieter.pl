from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       url(r'^index/$','dieter.managment.views.index', name='managment_index'),
                       url(r'^create_diet/$','dieter.managment.views.create_diet', name='managment_create_diet'),
                       url(r'^delete_diet/(?P<diet_id>[0-9]+)/$','dieter.managment.views.delete_diet', name='managment_delete_diet'),
)