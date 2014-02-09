from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User, Group
from digiapproval_project.apps.digiapproval.auth_decorators import login_required_super
from digiapproval_project.apps.digiapproval import models as approval_models
from digiapproval_project.apps.digiapproval.taskforms import AbstractForm, field_types
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
        if 'toggle_public' in request.POST:
            spec.public = not spec.public
            spec.save()
        elif 'create_dict' in request.POST:
            task_type = request.POST.get('new_dict', False)
            task = spec.spec.task_specs.get(
                            request.POST.get('task_name', "0xD161AC71VE"), False)
            if task and task_type in TASK_DICT_METHODS:
                task.set_data(task_data = AbstractForm.make_task_dict(task_type, 'APPROVER'))
                spec.save()
                return redirect('task_dict', spec_id, task.name)
        else:
            for field in ['owner', 'approvers', 'delegators']:
                spec.__setattr__(field, get_object_or_404(Group, id=request.POST.get(field+'-group', -1)))
            for field in ['name', 'description']:
                spec.__setattr__(field, request.POST.get('spec_'+field, spec.__getattribute__(field)))
        spec.save()
    return render(request, 'spec_builder/view_spec.html', {
        'spec_model': spec,
        'groups': Group.objects.all(),
        'task_dicts': {k: v[0] for k,v in TASK_DICT_METHODS.items()}
    })
    
@login_required_super
def connect_task(request, spec_id, task_name):
    """Controller for connection of taskforms (doesnt handle multichoice/exclusivechoice)"""
    spec_model = get_object_or_404(approval_models.WorkflowSpec,
                                id=spec_id)
    origin_task = spec_model.spec.task_specs.get(task_name)
    
    existing_error = new_error = None       
    if origin_task is None:
        raise Http404('Unknown or Illegal origin task')
    if request.method == "POST":
        if 'connect' in request.POST:
            next_task = spec_model.spec.task_specs.get(
                            request.POST.get('existing_task', "0xD161AC71VE"), False)
            if next_task and next_task.name != "Start": 
                origin_task.connect(next_task)
                spec_model.save()
                return redirect('view_spec', spec_id)
            else:
                existing_error="Illegal or incorrect connecting task"
        elif 'create' in request.POST:
            next_task = CONNECTABLE_TASKS.get(request.POST.get('new_task', False), False)
            task_label = request.POST.get('task_label', False)
            if next_task and task_label and len(task_label) is not 0 \
                    and task_label not in spec_model.spec.task_specs:
                
                next_task = next_task[1](spec_model.spec, task_label)
                origin_task.connect(next_task)
                spec_model.save()
                return redirect('view_spec', spec_id)
            else:
                new_error = "Illegal new task or invalid task name"
    
    return render(request, 'spec_builder/connect_task.html', {
        'spec_model': spec_model,
        'origin_task': origin_task,
        'existing_tasks': {k: type(v).__name__ for k, v in spec_model.spec.task_specs.items()},
        'legal_tasks': {k: (v[0],v[1].__name__) for k, v in CONNECTABLE_TASKS.items()},
        'existing_error': existing_error,
        'new_error': new_error,
    })
    

def task_dict(request, spec_id, task_name):
    """Generic handler for task_dict editing"""
    spec_model = get_object_or_404(approval_models.WorkflowSpec,
                                id=spec_id)
    task_spec = spec_model.spec.task_specs.get(task_name)
    
    if task_spec is None: raise Http404('Unknown or Illegal origin task')
    else: task_type = task_spec.data['task_data'].get('form', False)
        
    if request.method == "POST":
        if 'delete_dict' in request.POST:
            del task_spec.data['task_data']
            spec_model.save()
            return redirect('view_spec', spec_id)
        elif 'update_actor' in request.POST and request.POST.get('actor') in ['APPROVER', 'CUSTOMER']:
            task_spec.data['task_data']['actor'] = request.POST.get('actor')
            spec_model.save()
            return redirect('task_dict', spec_id, task_name)
    #redirect to appropriate task_dict controller
    if task_type in TASK_DICT_METHODS:
        return TASK_DICT_METHODS[task_type][1](request, spec_model, task_spec)
    else:
        return render(request, 'spec_builder/task_dict.html', {
            'spec_model': spec_model,
            'task': task_spec,
        })
    
def accept_agreement_dict(request, spec_model, task_spec):
    agreement = task_spec.get_data('task_data')['data'].get('agreement', 'No Agreement is configured')
    field = task_spec.get_data('task_data')['fields'].get('acceptance', {'label': 'Do you accept this agreement?',
                                                                         'mandatory': True,
                                                                         'type': 'checkbox',
                                                                         'value': False})
    if request.method == 'POST':
        if 'agreement' in request.POST and len(request.POST.get('agreement')) is not 0:
            agreement = request.POST.get('agreement')
            task_spec.get_data('task_data')['data']['agreement'] = agreement
        if 'label' in request.POST and len(request.POST.get('label')) is not 0:
            field['label'] = request.POST.get('label')
        if 'mandatory' in request.POST: field['mandatory'] = True
        else: field['mandatory'] = False
        task_spec.get_data('task_data')['fields']['acceptance'] = field
    spec_model.save()

    return render(request, 'spec_builder/taskforms/AcceptAgreementDict.html', {
        'spec_model': spec_model,
        'task': task_spec,
        'agreement': agreement,
        'field': field
    })
    
def field_entry_dict(request, spec_model, task_spec):
    fields = task_spec.get_data('task_data')['fields']
    if request.method == "POST":
        if 'new_field' in request.POST:
            name = request.POST.get('new_name', False)
            label = request.POST.get('new_label', False)
            ftype = request.POST.get('new_type', False)
            if 'new_mandatory' in request.POST: mandatory = True
            else: mandatory = False
            if name and label and len(name) is not 0 \
                and len(label) is not 0 and ftype in field_types:
                fields[name] = {'label': label, 'mandatory': mandatory,
                                'type': ftype, 'value': False}
        else:
            for field in fields:
                if field+'_delete' in request.POST:
                    del fields[field]
                    break
                label = request.POST.get(field+'_label', False)
                if label and len(label) is not 0:
                    fields[field]['label'] = label
                if field+'_mandatory' in request.POST:
                    fields[field]['mandatory'] = True
                else: fields[field]['mandatory'] = False
                if request.POST.get(field+'_type', False) in field_types:
                    fields[field]['type'] = request.POST.get(field+'_type')
        task_spec.get_data('task_data')['fields'] = fields
        spec_model.save()

    return render(request, 'spec_builder/taskforms/FieldEntryDict.html', {
        'spec_model': spec_model,
        'task': task_spec,
        'fields': task_spec.get_data('task_data')['fields'],
        'field_types': field_types
    })
    
def file_upload_dict(request, spec_model, task_spec):
    file_name_field = task_spec.get_data('task_data')['fields'].get('file_name', {
                                                        'label': 'Name of File: ', 'mandatory': True,
                                                        'type': 'text', 'value': "",})
    file_field = task_spec.get_data('task_data')['fields'].get('file', {
                                                        'label': 'Upload File:', 'mandatory': True,
                                                        'type': 'file', 'value': None, })
                                                        
    if 'mandatory' in request.POST: file_field['mandatory'] = file_name_field['mandatory'] = True
    else: file_field['mandatory'] = file_name_field['mandatory'] = False
    
    task_spec.get_data('task_data')['fields']['file'] = file_field
    task_spec.get_data('task_data')['fields']['file_name'] = file_name_field
    spec_model.save()
    print task_spec.get_data('task_data')
    
    return render(request, 'spec_builder/taskforms/FileUploadDict.html', {
        'spec_model': spec_model,
        'task': task_spec,
        'mandatory': file_field['mandatory']
    })
    
    
CONNECTABLE_TASKS = {
    'simple': ('Simple Task Node', taskspecs.Simple),
    'join': ('Blocking Join Node', taskspecs.Join)
}              
    
TASK_DICT_METHODS = {
    'file_upload': ('Upload a File', file_upload_dict),
    'accept_agreement': ('Accept an Agreement', accept_agreement_dict),
    'field_entry': ('Fill out Form Fields', field_entry_dict),
}


                                  
            
    
 
