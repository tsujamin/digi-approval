from django.conf.urls import patterns, url

from digiapproval_project.apps.digiapproval import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^register', views.register_customer, name='register')
)