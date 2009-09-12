from django.conf.urls.defaults import * #@UnusedWildImport

urlpatterns = patterns('',
                       
    # pages for editing diet
    url(r'^create/(?P<user_id>[0-9]+)/$','dieter.diet.views.edit.create', name='create_diet'),                       
    url(r'^edit/(?P<diet_id>[0-9]+)/$','dieter.diet.views.edit.edit', name='edit_diet'),
    url(r'^edit/(?P<diet_id>[0-9]+)/(?P<day>[0-9]+)/$','dieter.diet.views.edit.edit', name='edit_diet'),    
    url(r'^add_day/(?P<diet_id>[0-9]+)/$','dieter.diet.views.edit.add_day', name='diet_add_day'),
    url(r'^add_day/(?P<diet_id>[0-9]+)/(?P<day>[0-9]+)/$','dieter.diet.views.edit.add_day', name='diet_add_day'),
    url(r'^del_day/(?P<diet_id>[0-9]+)/$','dieter.diet.views.edit.del_day', name='diet_del_day'),
    url(r'^del_day/(?P<diet_id>[0-9]+)/(?P<day>[0-9]+)/$','dieter.diet.views.edit.del_day', name='diet_del_day'),
    url(r'^action/(?P<diet_id>[0-9]+)/(?P<sequence_no>[0-9]+)/$','dieter.diet.views.edit.perform_action', name='diet_perform_action'),
    url(r'^food/$','dieter.diet.views.edit.food_autocomplete',name="diet_food_autocomplete"),
    url(r'^send_diet/(?P<diet_id>[0-9]+)/$','dieter.diet.views.edit.send_diet', name='diet_send_form'),
    
    # diet dashboard
    url(r'^$','dieter.diet.views.view.index',name="diet"),
    url(r'^(\d{4})/(\d{1,2})/(\d{1,2})/$','dieter.diet.views.view.index', name='diet'),
    url(r'^print_diet/(?P<diet_id>[0-9]+)/$','dieter.diet.views.view.print_diet', name='diet_print_diet'),
    url(r'^print_diet/$','dieter.diet.views.view.print_diet', name='diet_print_diet'),
    url(r'^diet_start_day/(?P<diet_id>[0-9]+)/$','dieter.diet.views.view.diet_start_date', name='diet_start_date'),
    
    
)