from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User, Group
from digiapproval_project.apps.digiapproval.auth_decorators import login_required_super
from digiapproval_project.apps.digiapproval import models as approval_models
from SpiffWorkflow.specs import WorkflowSpec
from SpiffWorkflow import specs as taskspecs

def index(request):
    return redirect('home')

@login_required_super
def builder_home(request):
    """Shows a list of all system workflow specs (organised by owner) with ability to view/disable them"""
    if request.method == 'POST':
        spec = get_object_or_404(approval_models.WorkflowSpec, 
                                id=request.POST.get('spec', -1))
        if 'toggle_public' in request.POST:
            spec.public = not spec.public
            spec.save()
        elif 'edit' in request.POST:
            return redirect('view_spec', spec_id=spec.id)
    wf_spec_ordered = {} #{owner: [specs],...}
    for spec in approval_models.WorkflowSpec.objects.all():
        if spec.owner.name not in wf_spec_ordered: wf_spec_ordered[spec.owner.name] = []
        wf_spec_ordered[spec.owner.name].append(spec)
        
    return render(request, 'spec_builder/builder_home.html', {
        'spec_list': wf_spec_ordered,
    })
    
@login_required_super
def new_spec(request):
    if request.method == "POST":
        group = get_object_or_404(Group,
                                id=request.POST.get('spec_owner', -1))
        name = request.POST.get('spec_name', False)
        
        if len(request.POST.get('spec_desc', '')) is 0: desc = "No description provided"
        else: desc = request.POST.get('spec_desc', '')
        
        if name:
            spec_model = approval_models.WorkflowSpec(owner=group, 
                                                        approvers=group, 
                                                        delegators=group, 
                                                        name=name, 
                                                        public=False,
                                                        spec=WorkflowSpec(name), 
                                                        description=desc)
            spec_model.save()
            return redirect('view_spec', spec_id=spec_model.id)
    return render(request, 'spec_builder/new_spec.html', {
        'groups': Group.objects.all()
    })
    
@login_required_super
def view_spec(request, spec_id):
    spec = get_object_or_404(approval_models.WorkflowSpec,
                                id=spec_id)
    if request.method == "POST":
        print request.POST
        if 'toggle_public' in request.POST:
            spec.public = not spec.public
            spec.save()
            print spec.public
        else:
            for field in ['owner', 'approvers', 'delegators']:
                spec.__setattr__(field, get_object_or_404(Group, id=request.POST.get(field+'-group', -1)))
            for field in ['name', 'description']:
                spec.__setattr__(field, request.POST.get('spec_'+field, spec.__getattribute__(field)))
        spec.save()
    return render(request, 'spec_builder/view_spec.html', {
        'spec_model': spec,
        'groups': Group.objects.all()
    })
    
@login_required_super
def connect_task(request, spec_id, task_name):
    spec_model = get_object_or_404(approval_models.WorkflowSpec,
                                id=spec_id)
    origin_task = spec_model.spec.task_specs.get(task_name)
    if origin_task is None:
        raise Http404
    if request.method == "POST":
        pass
    
    return render(request, 'spec_builder/connect_task.html', {
        'spec_model': spec_model,
        'origin_task': origin_task
    })
                                

CONNECTABLE_TASKS = {
    'simple': taskspecs.Simple,
    'join': taskspecs.Join
}                                
            
    
 
