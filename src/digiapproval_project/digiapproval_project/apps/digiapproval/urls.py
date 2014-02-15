from django.conf.urls import patterns, url
from digiapproval_project.apps.digiapproval import views

urlpatterns = patterns(
    '',
    # main pages
    url(r'^$', views.index, name='index'),

    # Not yet implemented
    url(r'^settings/$', views.settings, name='settings'),

    url(r'^modify_subaccounts/$', views.modify_subaccounts,
        name='modify_subaccounts'),
    url(r'^remove_parentaccounts/$', views.remove_parentaccounts,
        name='remove_parentaccounts'),

    # applicants-only pages
    url(r'^applicant_home/$', views.applicant_home, name='applicant_home'),

    # staff-only pages
    url(r'^approver_worklist/$', views.approver_worklist,
        name='approver_worklist'),
    url(r'^delegator_worklist/$', views.delegator_worklist,
        name='delegator_worklist'),

    # workflows/tasks
    url(r'^view_workflow/(?P<workflow_id>\d+)/$', views.view_workflow,
        name='view_workflow'),
    url(r'^new_workflow/(?P<workflowspec_id>\d+)/$', views.new_workflow,
        name='new_workflow'),
    url(r'^workflow_spec/(?P<workflowspec_id>\d+)/svg$',
        views.view_workflowspec_svg, name='view_workflowspec_svg'),
    url(r'^view_task/(?P<workflow_id>\d+)/(?P<task_uuid>.+)/$',
        views.view_task, name='view_task'),
    url(r'^view_task_data/(?P<task_uuid>.+)/$', views.view_task_data,
        name='view_task_data'),
    url(r'^view_workflow_messages/(?P<workflow_id>\d+)/$',
        views.view_workflow_messages, name='view_workflow_messages'),
    url(r'^workflow_state/(?P<workflow_id>\d+)/$', views.workflow_state,
        name='update_workflow_state'),
    url(r'^workflow_label/(?P<workflow_id>\d+)/$', views.workflow_label,
        name='update_workflow_label'),

    url(r'^view_spec/(?P<spec_id>\d+)/svg/$', views.view_workflowspec_svg,
        kwargs={'fullsize': False}, name="view_workflowspec_svg"),
    url(r'^view_spec/(?P<spec_id>\d+)/svg/fullsize/$',
        views.view_workflowspec_svg,
        kwargs={'fullsize': True}, name="view_workflowspec_svg_fullsize"),

)
