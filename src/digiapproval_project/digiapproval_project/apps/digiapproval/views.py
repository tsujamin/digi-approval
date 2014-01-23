from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.shortcuts import get_object_or_404
from .forms import *
from .auth_decorators import *
from .models import *
import uuid
from SpiffWorkflow import Task

def index(request):
    return render(request, 'digiapproval/index.html')


def register_customer(request):
    """Creates CustomerUser and corresponding User if RegisterUserForm is valid"""
    if request.method == 'POST':
        form = RegisterCustomerForm(request.POST)
        if form.is_valid():
            account = form.create_customer()
            if account is not None:
                return HttpResponse("Account Successfully Created")
    else:
        form = RegisterCustomerForm()
    return render(request, 'digiapproval/register_customer.html', {
        'form' : form,
    })
    
def login(request):
    """Login controller for customer accounts, Currently doesnt display error on bad credentials"""
    from django.contrib.auth import login as auth_login
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        user = login_form.is_valid()
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect(reverse('index'))
    else:
        login_form = LoginForm()
    return render(request, 'digiapproval/login.html', {
        'form' : login_form,
    })
    
def logout(request):
    """Logs out any currently logged in user"""
    from django.contrib.auth import logout as auth_logout
    if request.user.is_authenticated():
        auth_logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required_organisation()
def modify_subaccounts(request):
    """ Controller for modify_subaccounts template. Requires an authenticated CustomerAccount of type ORGINISATION
        Currently doesnt return useful error messages """
    customer = request.user.customeraccount
    if request.method == 'POST':
        if request.POST.get('remove_account', False):
            customer.sub_accounts.remove(
                CustomerAccount.objects.get(id=request.POST['remove_account']))
        elif request.POST.get('add_account', False):
            try:
                customer.sub_accounts.add(
                    CustomerAccount.objects
                        .filter(user__username=request.POST['add_account'], account_type='CUSTOMER')[0])
            except:
                pass
        customer.save()    
    return render(request, 'digiapproval/modify_subaccounts.html', {
        'subaccounts' : customer.sub_accounts.all()
    })
    
@login_required_customer()
def remove_parentaccounts(request):
    """ Controller for remove_parentaccounts template. Requires authenticated CustomerAccount of type CUSTOMER
        Currently doesnt return useful error messages"""
    customer = request.user.customeraccount
    if request.method == 'POST' and request.POST.get('remove_account', False):
        customer.parent_accounts.remove(
            CustomerAccount.objects.get(id=request.POST['remove_account']))
        customer.save()
                
    return render(request, 'digiapproval/remove_parentaccounts.html', {
        'parentaccounts' : customer.parent_accounts.all()
    })
        


@login_required_customer()
def applicant_home(request):
    """Controller for applicant home page. Displays the applicant's current applications, as well as a list of workflow specs to start new applications.
    
    Requires authenticated CustomerAccount of type CUSTOMER.
    """
    customer = request.user.customeraccount
    return render(request, 'digiapproval/applicant_home.html', {
        'running_workflows_and_tasks' : map(lambda wf: (wf, wf.get_ready_task_forms(actor = 'CUSTOMER')), 
            customer.get_all_workflows(completed=False)),
        'completed_workflows' : customer.get_all_workflows(completed=True),
        'workflow_specs' : WorkflowSpec.objects.filter(public=True)
    })
    

@login_required()
def approver_worklist(request):
    """Controller for approver worklist. Displays the approver's worklist ... TODO Finish description
    
    Requires authenticated User with approver privileges on approval stages."""
    pass


@login_required()
def delegator_worklist(request):
    """Controller for delegator worklist. Displays... TODO Finish description
    
    Requires authenticated User with delegator privileges on approval stages.
    """
    pass


@login_required()
def view_workflow(request, workflow_id):
    """Controller for viewing workflows. TODO finish description
    TODO verify that this user is allowed to view.
    """
    # figure out what and who we are
    workflow = get_object_or_404(Workflow, pk=workflow_id)
    if request.user != workflow.customer.user and \
      request.user != workflow.approver:
        raise PermissionDenied

    try:
        customer = request.user.customeraccount
        actor = 'CUSTOMER'
    except:
        actor = 'APPROVER'

    
    
    # iterate through the tasks, making a list of actually useful information
    tasks_it = Task.Iterator(workflow.workflow.task_tree)
    # ... skip the root
    tasks_it.next()

    tasks = []
    for task in tasks_it:
        result = {
            'name': task.get_name(),
            'state_name': task.state_names[task.state],
            'actor': (task.task_spec.get_data('task_data')['actor'] if task.task_spec.get_data('task_data') else ''),
            'uuid': task.id['__uuid__']
            }

        # show a link if the task is ready and I can complete it.
        # TODO: extend to view past work (see todo in view_task)
        result['show_link'] = (task.state == task.READY and result['actor'] == actor)

        tasks.append(result)
    
    return render(request, 'digiapproval/view_workflow.html', {
        'workflow': workflow,
        'tasks': tasks
        })


@login_required_customer()
def new_workflow(request, workflowspec_id):
    """Controller for creating new workflows. TODO finish description
    """
    pass
    
def view_task(request, workflow_id, task_uuid):
    """Transient controller for returning appropriate taskform controller, authentication is handled by taskform
    """
    workflow = get_object_or_404(Workflow, pk=workflow_id)
    task_form_list = [task for task in workflow.get_ready_task_forms() if task.uuid == uuid.UUID(task_uuid)]
    if len(task_form_list) is 1:
        return task_form_list[0].form_request(request)
    else: #either invalid data or hash collision
        # TODO: display completed data if available.
        return HttpResponseRedirect(reverse('applicant_home'))
        
        
    
        
        
        

  
