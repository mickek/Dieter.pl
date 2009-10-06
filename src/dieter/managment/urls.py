from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       url(r'^index/$','dieter.managment.views.index', name='managment_index'),
                       url(r'^create_diet/$','dieter.managment.views.create_diet', name='managment_create_diet'),
)