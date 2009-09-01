from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$','dieter.home.views.index', name='index'),
    url(r'^logged_in$','dieter.home.views.logged_in', name="logged_in"),
    url(r'^complete_profile$','dieter.home.views.complete_profile', name="complete_profile")
)