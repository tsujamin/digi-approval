from django.conf.urls import patterns, url

from digiapproval_project.apps.spec_builder import views

urlpatterns = patterns(
    '',
    # main pages
    url(r'^$', views.index, name='index'),
    url(r'^builder_home/$', views.builder_home, name="home"),
    url(r'^new_spec/$', views.new_spec, name="new_spec"),
    url(r'^view_spec/(?P<spec_id>\d+)/$', views.view_spec, name="view_spec"),
)
