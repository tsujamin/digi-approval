from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.forms.formsets import formset_factory
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .forms import DelegatorBaseFormSet, DelegatorForm
from .auth_decorators import login_required_organisation,\
    login_required_customer, login_required_approver, login_required_delegator
from .models import WorkflowSpec, Workflow, Task, Message, CustomerAccount,\
    UserFile
import uuid
from SpiffWorkflow import Task as SpiffTask
import itertools
from django.core.urlresolvers import reverse
from .utils import never_cache
import networkx as nx
import re
from SpiffWorkflow.storage.NetworkXSerializer import NetworkXSerializer


## MAIN PAGES
def index(request):
    return render(request, 'digiapproval/index.html')


@login_required
def profile(request):
    """Handler for accounts/profile - which is where users are redirected after
    logging in. Redirect them onwards to somewhere more useful."""

    if hasattr(request.user, 'customeraccount'):
        if request.user.customeraccount.account_type == 'CUSTOMER':
            return redirect('applicant_home')
        else:
            return redirect('modify_subaccounts')

    # for user who is approver and delegator, default to approver_worklist
    if any([hasattr(g, 'workflowspecs_approvers')
            for g in request.user.groups.all()]):
        return redirect('approver_worklist')

    # for user who is approver and delegator, default to approver_worklist
    if any([hasattr(g, 'workflowspecs_delegators')
            for g in request.user.groups.all()]):
        return redirect('delegator_worklist')

    return HttpResponse("""You don't have a role in the DigiApproval system.
                        This is probably a bug, and we're very sorry - please
                        contact us.""")


@login_required
def settings(request):
    raise NotImplementedError


@login_required_organisation
def modify_subaccounts(request):
    """Controller for modify_subaccounts template. Requires an authenticated
    CustomerAccount of type ORGINISATION

    Currently doesn't return useful error messages."""
    customer = request.user.customeraccount
    if request.method == 'POST':
        if request.POST.get('remove_account', False):
            customer.sub_accounts.remove(
                CustomerAccount.objects.get(id=request.POST['remove_account']))
        elif request.POST.get('add_account', False):
            try:
                customer.sub_accounts.add(
                    CustomerAccount.objects
                        .filter(user__username=request.POST['add_account'],
                                account_type='CUSTOMER')[0])
            except:
                pass
        customer.save()
    return render(request, 'digiapproval/modify_subaccounts.html', {
        'subaccounts': customer.sub_accounts.all()
    })


@login_required_customer
def remove_parentaccounts(request):
    """Controller for remove_parentaccounts template. Requires authenticated
    CustomerAccount of type CUSTOMER.

    Currently doesnt return useful error messages"""
    customer = request.user.customeraccount
    if request.method == 'POST' and request.POST.get('remove_account', False):
        customer.parent_accounts.remove(
            CustomerAccount.objects.get(id=request.POST['remove_account']))
        customer.save()

    return render(request, 'digiapproval/remove_parentaccounts.html', {
        'parentaccounts': customer.parent_accounts.all()
    })


## APPLICANT-ONLY PAGES

@login_required_customer
@never_cache
def applicant_home(request):
    """Controller for applicant home page. Displays the applicant's current
    applications, as well as a list of workflow specs to start new
    applications.

    Requires authenticated CustomerAccount of type CUSTOMER.
    """
    customer = request.user.customeraccount
    return render(request, 'digiapproval/applicant_home.html', {
        'running_workflows_and_tasks': map(
            lambda wf: (wf, wf.get_ready_task_forms(actor='CUSTOMER'),
                        Message.get_unread_messages(wf, request.user).count()),
            customer.get_all_workflows(completed=False)),
        'completed_workflows': map(
            lambda wf: (wf,
                        Message.get_unread_messages(wf, request.user).count()),
            customer.get_all_workflows(completed=True)),
        'workflow_specs': WorkflowSpec.objects.filter(public=True,
                                                      toplevel=True)
    })


## STAFF-ONLY PAGES

@login_required_approver
@never_cache
def approver_worklist(request):
    """Controller for approver worklist. Displays the approver's worklist

    TODO Finish description

    Requires authenticated User with approver privileges on approval stages."""

    workflows = request.user.workflow_approver.filter(completed=False)
    running_workflows_and_tasks = map(
        lambda wf: (wf, wf.get_ready_task_forms(actor='APPROVER'),
                    Message.get_unread_messages(wf, request.user).count()),
        workflows)

    return render(request, 'digiapproval/approver_worklist.html', {
        'running_workflows_and_tasks': running_workflows_and_tasks,
    })


@login_required_delegator
@never_cache
def delegator_worklist(request):
    """Controller for delegator worklist. Displays... TODO Finish description

    Requires authenticated User with delegator privileges on approval stages.
    """
    message = None

    if (request.method == 'POST' and
            request.POST.get('delegate_workflows', False)):
        # TODO: do this much more nicely, error handling and all that
        spec = WorkflowSpec.objects.get(id=request.POST.get('spec_id', None))
        if spec.delegators not in request.user.groups.all():
            raise PermissionDenied

        DelegatorFormFormSet = formset_factory(DelegatorForm,
                                               formset=DelegatorBaseFormSet,
                                               max_num=0)
        approvers = [(approver.username, approver.get_full_name())
                     for approver in spec.approvers.user_set.all()]
        formset = DelegatorFormFormSet(request.POST, request.FILES,
                                       approvers=approvers)
        if formset.is_valid():
            for form_data in formset.cleaned_data:
                workflow = Workflow.objects.get(id=form_data['workflow_id'])
                approver = User.objects.get(username=form_data['approver'])
                if spec.approvers not in approver.groups.all():
                    raise PermissionDenied
                workflow.approver = approver
                workflow.save()
            message = "Approvers successfully updated."
        else:
            # TODO: better error handling
            message = "Error updating approvers."

    # Work out specs for which this user is delegator
    # get every group the user is in; get all of the specs for which that group
    # is responsible. Gives us a nested list.
    workflowspecs = [group.workflowspecs_delegators.all()
                     for group in request.user.groups.all()]
    # Flatten. Set is probably unnecessary because a workflow has at most one
    # group of delegators, so TODO verify necessary.
    workflowspecs = set(itertools.chain.from_iterable(workflowspecs))

    factory = formset_factory(DelegatorForm, formset=DelegatorBaseFormSet,
                              max_num=0)
    formsets = [{
        'formset': factory(
            approvers=[(approver.username, approver.get_full_name())
                       for approver in wfspec.approvers.user_set.all()],
            initial=[
                {'workflow_id': workflow.id,
                 'workflow_customer': workflow.customer.user.get_full_name(),
                 'workflow_customer_username': workflow.customer.user.username,
                 'approver': workflow.approver.username
                 } for workflow in wfspec.workflow_set.filter(completed=False)]
            ),
        'spec_name': wfspec.name,
        'spec_id': wfspec.id
        }
        for wfspec in workflowspecs]

    return render(request, 'digiapproval/delegator_worklist.html', {
        'formsets': formsets,
        'message': message
    })


## WORKFLOWS / TASKS

def view_workflowspec_svg(request, spec_id, fullsize=False):
    # TODO: Check public etc
    spec = get_object_or_404(WorkflowSpec, id=spec_id)

    graph = spec.to_coloured_graph()
    agraph = nx.to_agraph(graph)

    for nodename in agraph.nodes():
        del agraph.get_node(nodename).attr['data']

    svg = agraph.draw(None, 'svg', 'dot')
    # http://www.graphviz.org/content/percentage-size-svg-output
    if not fullsize:
        svg = re.sub(r'<svg width="[0-9]+pt" height="[0-9]+pt"',
                     r'<svg width="100%" height="100%"', svg)

    response = HttpResponse(svg, content_type="image/svg+xml")
    return response


@login_required
def view_workflow_svg(request, workflow_id, fullsize=False):
    workflow = get_object_or_404(Workflow, id=workflow_id)
    actor = workflow.actor_type(request.user)
    if actor is None:
        raise PermissionDenied()

    nxs = NetworkXSerializer()
    graph = nxs.serialize_workflow(workflow.workflow)

    for nodename in graph.nodes():
        node = graph.node[nodename]

        # standard fix
        node['label'] = node['label'].replace("\n", "\\n")

        # try to link them up
        target = None
        possible_tasks = workflow.workflow.get_tasks_from_spec_name(nodename)
        if any([task for task in possible_tasks
                if (task.state in (task.MAYBE,
                                   task.LIKELY,
                                   task.FUTURE))]):
            # never link to a task if it's been looped back on and is now in
            # some way pending
            continue

        # otherwise try to pick a ready or completed task
        for task in possible_tasks:
            if task.state == task.READY:
                # pick this one definitely
                target = task
                break
            elif task.state == task.COMPLETED and target is None:
                # pick the first one unless a Ready one comes up
                target = task

        if target is not None and 'task_data' in target.task_spec.data:
            #print target.task_spec.data['task_data']
            if target.state == target.READY and \
                    target.task_spec.data['task_data']['actor'] == actor:
                node['URL'] = reverse('view_task', kwargs={
                    'workflow_id': workflow_id,
                    'task_uuid': str(task.id['__uuid__'])})
                node['fontcolor'] = '#0000FF'
                node['target'] = '_parent'
            elif target.state == target.READY:  # other party - greyed out red
                node['fillcolor'] = '#AA4444'
            elif target.state == target.COMPLETED:
                node['URL'] = reverse('view_task_data', kwargs={
                    'task_uuid': str(task.id['__uuid__'])})
                node['fontcolor'] = '#0000FF'
                node['target'] = '_parent'

    agraph = nx.to_agraph(graph)

    svg = agraph.draw(None, 'svg', 'dot')
    # http://www.graphviz.org/content/percentage-size-svg-output
    if not fullsize:
        svg = re.sub(r'<svg width="[0-9]+pt" height="[0-9]+pt"',
                     r'<svg width="100%" height="100%"', svg)

    response = HttpResponse(svg, content_type="image/svg+xml")
    return response


def workflow_taskdata(workflow_id, actor):
    """Extracts task metadata from a workflow, for display in view_workflow"""
    workflow = Workflow.objects.get(pk=workflow_id)

    # iterate through the tasks, making a list of actually useful information
    tasks_it = SpiffTask.Iterator(workflow.workflow.task_tree)
    # ... skip the root
    tasks_it.next()

    tasks = []
    for task in tasks_it:
        result = {
            'name': task.get_name(),
            'state_name': task.state_names[task.state],
            'actor': (task.task_spec.get_data('task_data')['actor']
                      if task.task_spec.get_data('task_data') else ''),
            'form': (task.task_spec.get_data('task_data')['form']
                     if task.task_spec.get_data('task_data') else ''),
            'uuid': task.id['__uuid__'],
            'workflow_id': workflow_id,  # we need this in the result dict to
                                         # deal with links to subworkflows: AJD

            # if True, indent list AFTER printing current task
            'indent': False,
            # if True, dedent list AFTER printing current task
            'dedent': False,
            }

        # should various links be shown?
        result['show_task_link'] = (task.state == task.READY and
                                    result['actor'] == actor)
        result['show_data_link'] = (task.state == task.COMPLETED and
                                    result['actor'])

        # Filter (non completed/ready tasks from customers) and task with
        # task_dict
        if ((result['state_name'] == 'READY' or
             result['state_name'] == 'COMPLETED' or
             actor == 'APPROVER') and
                result['actor']):
            tasks.append(result)

            # Subworkflows
            if result['form'] == 'subworkflow':
                subworkflow_id = None
                try:
                    task_model = Task.objects.get(
                        uuid=uuid.UUID(result['uuid']))
                    subworkflow_id = task_model.task['data']['workflow_id']
                except:
                    pass

                if subworkflow_id:
                    tasks[-1]['indent'] = True
                    tasks.extend(workflow_taskdata(subworkflow_id, actor))
                    tasks[-1]['dedent'] = True

    return tasks


@never_cache
@login_required
def view_workflow(request, workflow_id):
    """Controller for viewing workflows. TODO finish description
    """
    # figure out what and who we are
    workflow = get_object_or_404(Workflow, pk=workflow_id)

    actor = workflow.actor_type(request.user)
    if actor is None:
        raise PermissionDenied

    # breadcrumb it
    request.breadcrumbs([portal_breadcrumb(workflow, request.user),
                         workflow_breadcrumb(workflow)])
    tasks = workflow_taskdata(workflow_id, actor)

    # mark all messages read
    Message.mark_all_read(workflow, request.user)

    return render(request, 'digiapproval/view_workflow.html', {
        'workflow': workflow,
        'tasks': tasks,
        'messages': workflow.message_set.order_by('id').reverse()[0:5],
        'user_type': actor
        })


@login_required_customer
def new_workflow(request, workflowspec_id):
    """Controller for creating new workflows. Displays information page about
    the requested WorkflowSpec, then creates new workflow when requested by
    user.

    Requires authenticated CustomerAccount of type CUSTOMER.
    """
    # TODO: creating organisational workflows
    # TODO: what's the best way to handle non-public workflows? And
    # non-top-level workflows?

    workflowspec = get_object_or_404(WorkflowSpec, id=workflowspec_id,
                                     public=True, toplevel=True)
    error = None

    customer = request.user.customeraccount
    permitted_accounts = [customer]
    for account in customer.parent_accounts.all():
        permitted_accounts.append(account)

    request.breadcrumbs([
        ('Applicant Portal', reverse('applicant_home')),
        ('New Workflow', request.path_info)
        ])

    if request.method == 'POST' and request.POST.get('create_workflow', False):
        acct_id = int(request.POST.get('account', None))
        wf_customer = get_object_or_404(CustomerAccount, id=acct_id)
        if wf_customer in permitted_accounts:
            workflow = workflowspec.start_workflow(wf_customer)
            label = request.POST.get('label', False)
            if label and len(label) > 0:
                workflow.label = label
            workflow.save()
            return redirect('view_workflow', workflow_id=workflow.id)
        error = "Please select a valid account"
    return render(request, 'digiapproval/new_workflow.html', {
        'workflowspec': workflowspec,
        'accounts': permitted_accounts,
        'error': error
    })


@login_required
@never_cache
def view_task(request, workflow_id, task_uuid):
    """Transient controller for returning appropriate taskform controller,
    authentication is handled by taskform
    """
    workflow = get_object_or_404(Workflow, pk=workflow_id)
    task_form_list = [task for task in workflow.get_ready_task_forms()
                      if task.uuid == uuid.UUID(task_uuid)]
    if len(task_form_list) is 1:
        task_form = task_form_list[0]
        request.breadcrumbs([
            portal_breadcrumb(workflow, request.user),
            workflow_breadcrumb(workflow),
            (task_form.spiff_task.get_name(), request.path_info)
            ])
        return task_form.form_request(request)
    else:  # either invalid data or hash collision
        # TODO: display completed data if available: redirect to view_task_data
        return redirect('applicant_home')


@login_required
def view_task_data(request, task_uuid):
    """ View the entered data of a completed task. """

    # figure out what and who we are
    task = get_object_or_404(Task, uuid=uuid.UUID(task_uuid))
    if not request.user in task.workflow.get_involved_users():
        raise PermissionDenied

    # TODO verify uuid.hex is what we want.
    spiff_task = task.workflow.workflow.get_task(
        {'__uuid__': uuid.UUID(task.uuid).hex})

    if spiff_task.state != spiff_task.COMPLETED:
        # TODO: throw some sort of error
        return HttpResponse("You can't view the data of a task that hasn't" +
                            " been completed.")

    request.breadcrumbs([
        portal_breadcrumb(task.workflow, request.user),
        workflow_breadcrumb(task.workflow),
        (spiff_task.get_name(), request.path_info)
        ])

    #iterates and replaces values of file fields with link
    for field in task.task['fields']:
        if task.task['fields'][field]['type'] == 'file':
            task_id = task.task['fields'][field]['value']
            user_file = get_object_or_404(UserFile, id=task_id)

            # TODO will this give an invalid URL if file is None?
            if user_file.file is not None:
                task.task['fields'][field]['value'] = user_file.file.url
            else:
                task.task['fields'][field]['value'] = user_file.virus_status

    return render(request, 'digiapproval/view_task_data.html',
                  {'task': task,
                   'spiff_task': spiff_task})


@login_required
@never_cache
def view_workflow_messages(request, workflow_id):
    """Controller for workflow_messages view. Creates new messages and renders
    current ones"""
    workflow = get_object_or_404(Workflow, id=workflow_id)

    #Check auth
    if not request.user in workflow.get_involved_users():
        raise PermissionDenied

    request.breadcrumbs([
        portal_breadcrumb(workflow, request.user),
        workflow_breadcrumb(workflow),
        ('Messages', request.path_info)
        ])

    Message.mark_all_read(workflow, request.user)
    if request.method == 'POST' and request.POST.get('new_message', False):
        new_message = Message(workflow=workflow,
                              sender=request.user,
                              message=request.POST.get('new_message', False)
                              )
        new_message.save()
        return redirect(request.META['HTTP_REFERER'])
    else:
        return render(request, 'digiapproval/view_workflow_messages.html', {
            'messages': workflow.message_set.order_by('id').reverse(),
            'workflow': workflow,
        })


@login_required
def workflow_state(request, workflow_id):
    """Controller for modification of workflow state"""
    workflow = get_object_or_404(Workflow, id=workflow_id)
    new_state = request.POST.get('wf_state', False)
    actor = workflow.actor_type(request.user)

    if request.method == 'POST':
        # a change other than approval requires confirmation
        if not (new_state == "APPROVED" or request.POST.get('confirm', False)):
            return render(request, "digiapproval/confirm_workflow_state.html",
                          {'workflow': workflow,
                           'new_state': new_state
                           })

        # attempt to change the state and notify
        try:
            workflow.change_state_by_user(new_state=new_state,
                                          user=request.user)
        except PermissionDenied, pd:
            raise pd
        except ValueError, ve:
            # TODO: render nicely.
            # this catches invalid states and invalid transitions
            return HttpResponse(str(ve))
        else:
            (_, nice_new_state) = filter(
                lambda (short, long): (short == new_state),
                Workflow.STATE_CHOICES)[0]
            Message(workflow=workflow, sender=request.user,
                    message=nice_new_state).save()
            Message.mark_all_read(workflow, request.user)

        if actor == 'CUSTOMER':
            return redirect('applicant_home')
        else:
            return redirect(request.META['HTTP_REFERER'])
    return redirect('view_workflow', workflow_id=workflow.id)


@login_required_customer
def workflow_label(request, workflow_id):
    workflow = get_object_or_404(Workflow, id=workflow_id)
    if not workflow.is_authorised_customer(request.user.customeraccount):
        raise PermissionDenied()

    new_label = request.POST.get('label', False)
    if request.method == 'POST' and new_label:
        workflow.label = new_label
        workflow.save()

    if hasattr(request.META, 'HTTP_REFERER'):
        return redirect(request.META['HTTP_REFERER'])
    else:
        return redirect('view_workflow', workflow_id=workflow_id)


def portal_breadcrumb(workflow, user):
    actor = workflow.actor_type(user)
    if actor == 'CUSTOMER':
        return ('Applicant Portal', reverse('applicant_home'))
    elif actor == 'APPROVER':
        return ('Approver Worklist', reverse('approver_worklist'))
    else:
        raise PermissionDenied


def workflow_breadcrumb(workflow):
    return (workflow.label,
            reverse('view_workflow', kwargs={'workflow_id': workflow.id}))
