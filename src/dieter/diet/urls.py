from django.conf.urls.defaults import * #@UnusedWildImport

urlpatterns = patterns('',
                       
    # pages for editing diet
    url(r'^create/(?P<user_id>[0-9]+)/$','dieter.diet.views.edit.create', name='create_diet'),
    url(r'^edit/$','dieter.diet.views.edit.edit_for_user', name='edit_diet_user'),
    url(r'^edit/(?P<day>[0-9]+)/$','dieter.diet.views.edit.edit_for_user', name='edit_diet_user'),    
    url(r'^a/edit/(?P<diet_id>[0-9]+)/$','dieter.diet.views.edit.edit_for_admin', name='edit_diet'),    # /s/ for staff
    url(r'^a/edit/(?P<diet_id>[0-9]+)/(?P<day>[0-9]+)/$','dieter.diet.views.edit.edit_for_admin', name='edit_diet'),
    url(r'^add_day/(?P<diet_id>[0-9]+)/$','dieter.diet.views.edit.add_day', name='diet_add_day'),
    url(r'^add_day/(?P<diet_id>[0-9]+)/(?P<day>[0-9]+)/$','dieter.diet.views.edit.add_day', name='diet_add_day'),
    url(r'^del_day/(?P<diet_id>[0-9]+)/$','dieter.diet.views.edit.del_day', name='diet_del_day'),
    url(r'^del_day/(?P<diet_id>[0-9]+)/(?P<day>[0-9]+)/$','dieter.diet.views.edit.del_day', name='diet_del_day'),
    url(r'^action/(?P<diet_id>[0-9]+)/(?P<sequence_no>[0-9]+)/$','dieter.diet.views.edit.perform_action', name='diet_perform_action'),
    url(r'^food/$','dieter.diet.views.edit.food_autocomplete',name="diet_food_autocomplete"),
    url(r'^s/send_diet/(?P<diet_id>[0-9]+)/$','dieter.diet.views.edit.send_diet', name='diet_send_form'),
    
    # diet dashboard
    url(r'^$','dieter.diet.views.view.index', name="diet"),
    url(r'^(\d{4})/(\d{1,2})/(\d{1,2})/$','dieter.diet.views.view.index', name='diet'),
    url(r'^print/(?P<diet_id>[0-9]+)/$','dieter.diet.views.view.print_diet', name='diet_print_diet'),
    url(r'^print/$','dieter.diet.views.view.print_diet', name='diet_print_diet'),
    url(r'^start_day/(?P<diet_id>[0-9]+)/$','dieter.diet.views.view.diet_start_date', name='diet_start_date'),
    
    url(r'^choose/$','dieter.diet.views.view.choose_diet', name="diet_choose_diet"),
    url(r'^choose_first_time/$','dieter.diet.views.view.choose_diet', {'initial':True}, name="diet_choose_diet_first_time"),
    
    url(r'^details/(?P<diet_id>[0-9]+)/$','dieter.diet.views.view.diet_details', name="diet_details"),
    url(r'^details/$','dieter.diet.views.view.diet_details', name="diet_details"), # required for generation of js urls
    
    url(r'^set/(?P<diet_id>[0-9]+)/$','dieter.diet.views.view.set_diet', name="diet_set"),
    
    
)