from django.conf.urls import patterns, url

from digiapproval_project.apps.digiapproval import views

urlpatterns = patterns('',
    
    # main pages
    url(r'^$', views.index, name='index'),
    
    # authentication/user settings
    url(r'^register', views.register_customer, name='register'),
    url(r'^login', views.login, name='login'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^settings', views.settings, name='settings'), # Not yet implemented
    url(r'^modify_subaccounts', views.modify_subaccounts, name='modify_subaccounts'),
    url(r'^remove_parentaccounts', views.remove_parentaccounts, name='remove_parentaccounts'),
    
    # applicants-only pages
    url(r'^applicant_home', views.applicant_home, name='applicant_home'),
    
    # staff-only pages
    url(r'^approver_worklist', views.approver_worklist, name='approver_worklist'),
    url(r'^delegator_worklist', views.delegator_worklist, name='delegator_worklist'),
    
    # workflows/tasks
    url(r'^view_workflow/(?P<workflow_id>\d+)$', views.view_workflow, name='view_workflow'),
    url(r'^new_workflow/(?P<workflowspec_id>\d+)$', views.new_workflow, name='new_workflow'),
    url(r'^view_task/(?P<workflow_id>\d+)/(?P<task_uuid>.+)$', views.view_task, name='view_task'),
    url(r'^view_task_data/(?P<task_uuid>.+)$', views.view_task_data, name='view_task_data'),
    url(r'^view_workflow_messages/(?P<workflow_id>\d+)$', views.view_workflow_messages, name='view_workflow_messages'),    
)
