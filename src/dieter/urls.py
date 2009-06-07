from django.conf import settings
from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
import os

admin.autodiscover()

urlpatterns = patterns('',
    url('', include('dieter.home.urls')),
    url('^dashboard/', include('dieter.dashboard.urls')),      
    url(r'^accounts/', include('dieter.registration.urls')),
    url(r'^admin/(.*)', admin.site.root),
)

#in local mode, media files are served this way
if settings.MEDIA_ROOT != '' and \
   settings.MEDIA_URL.startswith('/') and \
   settings.ADMIN_MEDIA_PREFIX.startswith('/'):
    urlpatterns += patterns('',
        (r'^' + settings.MEDIA_URL[1:] + r'(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        (r'^' + settings.ADMIN_MEDIA_PREFIX[1:] + r'(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.abspath(os.path.join(settings.DJANGO_PATH, 'contrib/admin/media/'))}),
    )
