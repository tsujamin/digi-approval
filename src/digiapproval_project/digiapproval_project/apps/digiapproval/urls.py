from django.conf.urls import patterns, url

from digiapproval_project.apps.digiapproval import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^register', views.register_customer, name='register'),
    url(r'^login', views.login, name='login'),
    url(r'^logout', views.logout, name='logout')
)