from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.forms.formsets import formset_factory
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .forms import RegisterCustomerForm, LoginForm, DelegatorBaseFormSet,\
    DelegatorForm
from .auth_decorators import login_required_organisation,\
    login_required_customer, login_required_approver, login_required_delegator
from .auth_functions import workflow_actor_type, workflow_authorised_customer
from .models import WorkflowSpec, Workflow, Task, Message, CustomerAccount,\
    UserFile
import uuid
from SpiffWorkflow import Task as SpiffTask
import itertools


## MAIN PAGES
def index(request):
    return render(request, 'digiapproval/index.html')


## AUTHENTICATION / USER SETTINGS

def register_customer(request):
    """Creates CustomerUser and corresponding User if RegisterUserForm
    is valid"""
    if request.method == 'POST':
        form = RegisterCustomerForm(request.POST)
        if form.is_valid():
            account = form.create_customer()
            if account is not None:
                return HttpResponse("Account Successfully Created")
    else:
        form = RegisterCustomerForm()
    return render(request, 'digiapproval/register_customer.html', {
        'form': form,
    })


def login(request):
    """Login controller for customer accounts."""
    from django.contrib.auth import login as auth_login
    error = None
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        user = login_form.is_valid()
        if user is not None:
            auth_login(request, user)
            if request.GET.get('next', None):
                return redirect(request.GET.get('next'))
            return redirect('index')
        else:
            error = "Bad username/password combination"
    return render(request, 'digiapproval/login.html', {
        'form':  LoginForm(),
        'error': error
    })


def logout(request):
    """Logs out any currently logged in user"""
    from django.contrib.auth import logout as auth_logout
    if request.user.is_authenticated():
        auth_logout(request)
    return redirect('index')


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
@login_required
def view_workflow(request, workflow_id):
    """Controller for viewing workflows. TODO finish description
    """
    # figure out what and who we are
    workflow = get_object_or_404(Workflow, pk=workflow_id)

    actor = workflow_actor_type(request.user, workflow)

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
            'uuid': task.id['__uuid__']
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
def view_task(request, workflow_id, task_uuid):
    """Transient controller for returning appropriate taskform controller,
    authentication is handled by taskform
    """
    workflow = get_object_or_404(Workflow, pk=workflow_id)
    task_form_list = [task for task in workflow.get_ready_task_forms()
                      if task.uuid == uuid.UUID(task_uuid)]
    if len(task_form_list) is 1:
        return task_form_list[0].form_request(request)
    else:  # either invalid data or hash collision
        # TODO: display completed data if available: redirect to view_task_data
        return redirect('applicant_home')


@login_required
def view_task_data(request, task_uuid):
    """ View the entered data of a completed task. """

    # figure out what and who we are
    task = get_object_or_404(Task, uuid=uuid.UUID(task_uuid))
    if request.user != task.workflow.customer.user and \
       request.user != task.workflow.approver:
        raise PermissionDenied

    # TODO verify uuid.hex is what we want.
    spiff_task = task.workflow.workflow.get_task(
        {'__uuid__': uuid.UUID(task.uuid).hex})

    if spiff_task.state != spiff_task.COMPLETED:
        # TODO: throw some sort of error
        return HttpResponse("You can't view the data of a task that hasn't" +
                            " been completed.")

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
def view_workflow_messages(request, workflow_id):
    """Controller for workflow_messages view. Creates new messages and renders
    current ones"""
    workflow = get_object_or_404(Workflow, id=workflow_id)

    #Check auth
    if not request.user in workflow.get_involved_users():
        raise PermissionDenied

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
    actor = workflow_actor_type(request.user, workflow)
    new_state = request.POST.get('wf_state', False)
    states = map(lambda (choice, _): (choice), Workflow.STATE_CHOICES)

    if request.method == 'POST' and new_state in states:
        (_, nice_new_state) = filter(
            lambda (short, long): (short == new_state),
            Workflow.STATE_CHOICES)[0]

        # a customer can only cancel an application
        if actor == 'CUSTOMER' and new_state != 'CANCELLED':
            raise PermissionDenied

        workflow.state = new_state
        if workflow.state == 'STARTED':
            workflow.completed = False
        else:
            workflow.completed = True
        workflow.save()
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
    if not workflow_authorised_customer(request.user.customeraccount,
                                        workflow):
        raise PermissionDenied()

    new_label = request.POST.get('label', False)
    if request.method == 'POST' and new_label:
        workflow.label = new_label
        workflow.save()
    return redirect(request.META['HTTP_REFERER'])
