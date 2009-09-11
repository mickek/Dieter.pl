from django.conf.urls.defaults import * #@UnusedWildImport

urlpatterns = patterns('',
    url(r'^$','dieter.inbox.views.index', name='inbox'),
)