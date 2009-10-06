from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       url(r'^index/$','dieter.managment.views.index', name='managment_index'),
)