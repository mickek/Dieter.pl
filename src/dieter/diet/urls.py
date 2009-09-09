from django.conf.urls.defaults import * #@UnusedWildImport

urlpatterns = patterns('',
                       
    # pages for editing diet
    url(r'^create/(?P<user_id>[0-9]+)/$','dieter.diet.views.create', name='create_diet'),                       
    url(r'^edit/(?P<diet_id>[0-9]+)/$','dieter.diet.views.edit', name='edit_diet'),
    url(r'^edit/(?P<diet_id>[0-9]+)/(?P<day>[0-9]+)/$','dieter.diet.views.edit', name='edit_diet'),    
    url(r'^add_day/(?P<diet_id>[0-9]+)/$','dieter.diet.views.add_day', name='diet_add_day'),
    url(r'^add_day/(?P<diet_id>[0-9]+)/(?P<day>[0-9]+)/$','dieter.diet.views.add_day', name='diet_add_day'),
    url(r'^del_day/(?P<diet_id>[0-9]+)/$','dieter.diet.views.del_day', name='diet_del_day'),
    url(r'^del_day/(?P<diet_id>[0-9]+)/(?P<day>[0-9]+)/$','dieter.diet.views.del_day', name='diet_del_day'),
    url(r'^action/(?P<diet_id>[0-9]+)/(?P<sequence_no>[0-9]+)/$','dieter.diet.views.perform_action', name='diet_perform_action'),
    url(r'^food/$','dieter.diet.views.food_autocomplete',name="diet_food_autocomplete"),
    
    # diet dashboard
    url(r'^$','dieter.diet.views.index',name="diet"),
    url(r'^(\d{4})/(\d{1,2})/(\d{1,2})/$','dieter.diet.views.index', name='diet'),
    url(r'^diet_start_day/(?P<diet_id>[0-9]+)/$','dieter.diet.views.diet_start_date', name='diet_start_date'),
    
)