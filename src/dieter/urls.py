from django.conf import settings
from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
import os

admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('dieter.home.urls')),
    url(r'^dashboard/', include('dieter.dashboard.urls')),
    url(r'^patients/', include('dieter.patients.urls')),      
    url(r'^accounts/', include('dieter.registration.urls')),
    url(r'^diet/', include('dieter.diet.urls')),
    url(r'^shopping/', include('dieter.shopping.urls')),
    url(r'^graphs/', include('dieter.graphs.urls')),
    url(r'^inbox/', include('dieter.inbox.urls')),
    
    url(r'^comments/', include('django.contrib.comments.urls')),    
    url(r'^admin/(.*)', admin.site.root),
)

if settings.MEDIA_ROOT != '' and \
    settings.MEDIA_URL.startswith('/') and \
    settings.ADMIN_MEDIA_PREFIX.startswith('/'):
        urlpatterns += patterns('',
            (r'^' + settings.MEDIA_URL[1:] + r'(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
            (r'^' + settings.ADMIN_MEDIA_PREFIX[1:] + r'(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.abspath(os.path.join(settings.DJANGO_PATH, 'contrib/admin/media/'))}),
        )
