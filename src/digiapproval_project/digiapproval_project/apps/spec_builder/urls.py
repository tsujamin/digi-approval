from django.conf.urls import patterns, url

from digiapproval_project.apps.spec_builder import views

urlpatterns = patterns(
    '',
    # main pages
    url(r'^$', views.index, name='index'),
    url(r'^builder_home/$', views.builder_home, name="builder_home"),
    url(r'^new_spec/$', views.new_spec, name="new_spec"),
    url(r'^view_spec/(?P<spec_id>\d+)/$', views.view_spec, name="view_spec"),
    url(r'^view_spec/(?P<spec_id>\d+)/svg/$', views.view_spec_svg,
        kwargs={'fullsize': False}, name="view_spec_svg"),
    url(r'^view_spec/(?P<spec_id>\d+)/svg/fullsize/$', views.view_spec_svg,
        kwargs={'fullsize': True}, name="view_spec_svg_fullsize"),
    url(r'^connect_task/(?P<spec_id>\d+)/(?P<task_name>.+)/$',
        views.connect_task_controller, name="connect_task"),
    url(r'^task_dict/(?P<spec_id>\d+)/(?P<task_name>.+)/$', views.task_dict,
        name="task_dict"),  
    url(r'^delete_task/(?P<spec_id>\d+)/(?P<task_name>.+)/$', 
        views.delete_task, name="delete_task"),
    url(r'^disconnect_task/(?P<spec_id>\d+)/(?P<task_name>.+)/$', 
        views.disconnect_task, name="disconnect_task"),
)
