from django.conf.urls import patterns, url

from digiapproval_project.apps.digiapproval import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^register', views.register_customer, name='register'),
    url(r'^login', views.login, name='login'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^modify_subaccounts', views.modify_subaccounts, name="modify_subaccounts"),
    url(r'^remove_parentaccounts', views.remove_parentaccounts, name="remove_parentaccounts")
)