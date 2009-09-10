from django.conf.urls.defaults import * #@UnusedWildImport

urlpatterns = patterns('',
    url(r'^$','dieter.shopping.views.index', name='shopping'),
    url(r'^(day|week)/$','dieter.shopping.views.index', name='shopping'),
    url(r'^print/(day|week)/$','dieter.shopping.views.print_list', name='shopping_print_list'),
)