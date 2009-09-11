from django.conf.urls.defaults import * #@UnusedWildImport

urlpatterns = patterns('',
    url(r'^$','dieter.graphs.views.index', name='graphs'),
    url(r'^(week|month|all)/$','dieter.graphs.views.index',name='graphs',),
)