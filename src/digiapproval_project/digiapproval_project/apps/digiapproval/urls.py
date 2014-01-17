from django.conf.urls import patterns, url

from digiapproval_project.apps.digiapproval import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^register', views.register_customer, name='register'),
    url(r'^login', views.login, name='login'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^modify_subaccounts', views.modify_subaccounts, name='modify_subaccounts'),
    url(r'^remove_parentaccounts', views.remove_parentaccounts, name='remove_parentaccounts'),
    url(r'^applicant_home', views.applicant_home, name='applicant_home'),
    url(r'^approver_worklist', views.approver_worklist, name='approver_worklist'),
    url(r'^delegator_worklist', views.delegator_worklist, name='delegator_worklist'),
    url(r'^view_workflow/(?P<workflow_id>\d+)$', views.view_workflow, name='view_workflow'),
    url(r'^new_workflow/(?P<workflowspec_id>\d+)$', views.new_workflow, name='new_workflow'),
)