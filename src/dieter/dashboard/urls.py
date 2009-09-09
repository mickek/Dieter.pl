from django.conf.urls.defaults import * #@UnusedWildImport

urlpatterns = patterns('',
    url(r'^$','dieter.dashboard.views.index', name='dashboard'),
    url(r'^(\d{4})/(\d{1,2})/(\d{1,2})/$','dieter.dashboard.views.index', name='dashboard'),
    url(r'^save_weight/(\d{4})/(\d{1,2})/(\d{1,2})/$', 'dieter.dashboard.views.save_weight', name='dashboard_save_weight')    
)