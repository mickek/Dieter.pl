from django.conf.urls.defaults import * #@UnusedWildImport

urlpatterns = patterns('',
    url(r'^$','dieter.shopping.views.agregated_meal_data', name='shopping'),
    url(r'^(day|week)/$','dieter.shopping.views.agregated_meal_data',name='shopping',),
    url(r'^print$','dieter.shopping.views.agregated_meal_data', {'template_name':'print.html'}, name='shopping_print_list'),
    url(r'^print/(day|week)/$','dieter.shopping.views.agregated_meal_data', {'template_name':'print.html'}, name='shopping_print_list'),
)