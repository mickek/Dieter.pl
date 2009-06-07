from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$','dieter.home.views.index', name='index'),
    url(r'^logged_in$','dieter.home.views.logged_in', name="logged_in")
)