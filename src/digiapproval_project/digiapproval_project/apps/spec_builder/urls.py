from django.conf.urls import patterns, url

from digiapproval_project.apps.spec_builder import views

urlpatterns = patterns(
    '',
    # main pages
    url(r'^$', views.index, name='index'),
    url(r'^builder_home/$', views.builder_home, name="home")
)
