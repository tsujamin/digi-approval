from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User, Group
from digiapproval_project.apps.digiapproval.auth_decorators import login_required_super
from digiapproval_project.apps.digiapproval import models as approval_models
from digiapproval_project.apps.digiapproval.taskforms import AbstractForm, field_types
from SpiffWorkflow.specs import WorkflowSpec
from SpiffWorkflow import specs as taskspecs
import networkx as nx
from SpiffWorkflow.storage.NetworkXSerializer import NetworkXSerializer
from django.core.urlresolvers import reverse

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
    """Creates new task from provided group and name"""
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
def view_spec_svg(request, spec_id):
    spec = get_object_or_404(approval_models.WorkflowSpec,
                                id=spec_id)
    nxs = NetworkXSerializer()
    graph = nxs.serialize_workflow_spec(spec.spec)
    agraph = nx.to_agraph(g)

    for nodename in agraph.nodes():
        node = agraph.get_node(nodename)
        node.attr.update(
            {'URL': reverse('task_dict', kwargs={
                'spec_id': spec.id,
                'task_name': str(node)}),
            'fontcolor': '#0000FF',
            'data': {},
            })
        node.attr['label'] = node.attr['label'].replace("\n", "\\n")

    response = HttpResponse(ag.draw(None, 'svg', 'dot'),
                            content_type="image/svg+xml")
    return response

    
@login_required_super
def view_spec(request, spec_id):
    """Controller for spec view, handles creation of new task_dicts and redirection to connect/task_dict edit pages"""
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
        'task_dicts': {k: v[0] for k,v in TASK_DICT_METHODS.items() if k not in CONNECTABLE_TASKS}
    })
    
@login_required_super
def connect_task_controller(request, spec_id, task_name):
    """Controller for connection of taskforms (doesnt handle multichoice/exclusivechoice)"""
    spec_model = get_object_or_404(approval_models.WorkflowSpec,
                                id=spec_id)
    origin_task = spec_model.spec.task_specs.get(task_name)
    
    if origin_task is None:
        raise Http404('Unknown or Illegal origin task')
    
    #Test for special connect_method for the taskform of origin_task (IE branching taskforms)
    origin_task_form = origin_task.data.get('task_data',{}).get('form', None)
    (_,_,connect_method) = CONNECTABLE_TASKS.get(origin_task_form, (None,None, None))
    if connect_method: return connect_method(request, spec_model, origin_task)
    
    error = None       
    
    if request.method == "POST":
        if 'connect' in request.POST:
            next_task = get_existing_task_from_request(request, spec_model)
            if not next_task: error="Illegal or incorrect connecting task" #        
        elif 'create' in request.POST:
            next_task = create_task_from_request(request, spec_model)
            if not next_task: error = "Illegal new task or invalid task name"
        if not error:        
            origin_task.connect(next_task)
            spec_model.save()
            return redirect('view_spec', spec_id)
    
    return render(request, 'spec_builder/connect_task.html', {
        'spec_model': spec_model,
        'origin_task': origin_task,
        'existing_tasks': {k: type(v).__name__ for k, v in spec_model.spec.task_specs.items()},
        'legal_tasks': {k: (v[0],v[1].__name__) for k, v in CONNECTABLE_TASKS.items()},
        'error': error,
    })

def get_existing_task(task_name, spec_model):
    """Gets existing task from workflow spec"""
    next_task = spec_model.spec.task_specs.get(task_name, False)
    if next_task and next_task.name != "Start": 
        return next_task

def get_existing_task_from_request(request, spec_model):
    """Connects task from given request (connect_task extending) and returns it """    
    return get_existing_task(
                    request.POST.get('existing_task', "0xD161AC71VE"),
                    spec_model)

def create_task(task_name, task_label, spec_model):
    """Creates new task using provided parameters"""
    next_task = CONNECTABLE_TASKS.get(task_name, False)
        
    if next_task and task_label and len(task_label) is not 0 \
            and task_label not in spec_model.spec.task_specs: 
        new_task = next_task[1](spec_model.spec, task_label)
        if next_task[2]: #Special connect method
            #Set newely created task to type of task (ie choose_branch)
            new_task.set_data(task_data=AbstractForm.make_task_dict( 
                task_name, 'APPROVER'))
        return new_task    
        
def create_task_from_request(request, spec_model):
    """creates task from request (connect_task extending) and returns it"""
    task_name = request.POST.get('new_task', False)
    task_label = request.POST.get('task_label', False)
    return create_task(task_name, task_label, spec_model)

def task_dict(request, spec_id, task_name):
    """Generic handler for task_dict editing"""
    spec_model = get_object_or_404(approval_models.WorkflowSpec,
                                id=spec_id)
    task_spec = spec_model.spec.task_specs.get(task_name)
    error = None
    
    if task_spec is None: raise Http404('Unknown or Illegal origin task')
    else: task_type = task_spec.data['task_data'].get('form', False)
    if request.method == "POST":
        if 'delete_dict' in request.POST:
            if task_type in CONNECTABLE_TASKS:
                error = "Cannot delete this type of task"
            else:
                del task_spec.data['task_data']
                spec_model.save()
                return redirect('view_spec', spec_id)
        elif 'update_general' in request.POST and request.POST.get('actor') in ['APPROVER', 'CUSTOMER']:
            task_spec.data['task_data']['actor'] = request.POST.get('actor')
            task_spec.data['task_data']['data']['task_info'] = request.POST.get('task_info')
            
            spec_model.save()
            return redirect('task_dict', spec_id, task_name)
    #redirect to appropriate task_dict controller
    if task_type in TASK_DICT_METHODS:
        return TASK_DICT_METHODS[task_type][1](request, spec_model, task_spec)
    else:
        return render(request, 'spec_builder/task_dict.html', {
            'spec_model': spec_model,
            'task': task_spec,
            'general_error': error
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
    
def choose_branch_connect(request, spec_model, origin_task):
    """Controller for creation of exclusivechoice choose_branch taks"""
    error = None       
    
    if request.method == "POST":
        label = request.POST.get('label', '')
        if label ==  '': #missing label
            error = "Must have label for choice"
        elif 'connect' in request.POST:
            next_task = get_existing_task_from_request(request, spec_model)
            if not next_task or next_task in origin_task.outputs: 
                error="Illegal or incorrect connecting task" #        
        elif 'create' in request.POST:
            next_task = create_task_from_request(request, spec_model)
            if not next_task or next_task in origin_task.outputs: 
                error = "Illegal new task or invalid task name"
        if not error:        
            from SpiffWorkflow.operators import Attrib, Equal
            
            task_number = len(origin_task.outputs)
            origin_task.connect_if(Equal(Attrib('selection'), task_number), next_task)
            if task_number is 0: #default branch
                origin_task.connect(next_task)
                
            origin_task.data['task_data']['fields'][next_task.name] = {
                'label': label, 'mandatory': False,
                'type': 'radio', 'value': False, 'number': task_number
            }    
                
            spec_model.save()
            return redirect('view_spec', spec_model.id)
    
    return render(request, 'spec_builder/taskforms/ChooseBranchConnect.html', {
        'spec_model': spec_model,
        'origin_task': origin_task,
        'existing_tasks': {k: type(v).__name__ for k, v in spec_model.spec.task_specs.items()},
        'legal_tasks': {k: (v[0],v[1].__name__) for k, v in CONNECTABLE_TASKS.items()},
        'error': error,
    })
    
def choose_branches_connect(request, spec_model, origin_task):
    """Controller for posting mutlichoice choose_branches tasks (pretty much copypasta of above)"""
    error = None       
    
    if request.method == "POST":
        label = request.POST.get('label', '')
        if label ==  '': #missing label
            error = "Must have label for choice"
        elif 'connect' in request.POST:
            next_task = get_existing_task_from_request(request, spec_model)
            if not next_task or next_task in origin_task.outputs: 
                error="Illegal or incorrect connecting task" #        
        elif 'create' in request.POST:
            next_task = create_task_from_request(request, spec_model)
            if not next_task or next_task in origin_task.outputs: 
                error = "Illegal new task or invalid task name"
        if not error:        
            from SpiffWorkflow.operators import Attrib, Equal
            
            task_number = len(origin_task.outputs)            
            origin_task.connect_if(Equal(Attrib("task" + str(task_number)), True), next_task)
            
            origin_task.data['task_data']['fields'][next_task.name] = {
                'label': label, 'mandatory': False,
                'type': 'checkbox', 'value': False, 'number': task_number
            }    
                
            spec_model.save()
            return redirect('view_spec', spec_model.id)
    
    return render(request, 'spec_builder/taskforms/ChooseBranchesConnect.html', {
        'spec_model': spec_model,
        'origin_task': origin_task,
        'existing_tasks': {k: type(v).__name__ for k, v in spec_model.spec.task_specs.items()},
        'legal_tasks': {k: (v[0],v[1].__name__) for k, v in CONNECTABLE_TASKS.items()},
        'error': error,
    })
    
def choose_branches_dict(request, spec_model, task_spec):
    if 'choices' in request.POST:
        task_spec.get_data('task_data')['options']['minimum_choices'] = int(request.POST.get('choices'))
        spec_model.save()

    return render(request, 'spec_builder/taskforms/ChooseBranchesDict.html', {
        'spec_model': spec_model,
        'task': task_spec,
        'choices': task_spec.get_data('task_data')['options'].get('minimum_choices', 0)
    })
    
def check_tally_connect(request, spec_model, origin_task):
    """Controller for connecting to check_tally"""
    error = None
    completed = not (len(origin_task.outputs) is 0) #if outputs is not 0, assume connect task completed
    if request.method == "POST" and not completed:
        new_tasks = {}
        for task_type in ['success', 'fail']:
            post_task_type = request.POST.get((task_type + '_task'), '')
            if post_task_type == (task_type + '_existing_task'): #if connecting to existing:
                new_tasks[task_type] = get_existing_task(request.POST.get(task_type + '_existing_task', None), spec_model)
            elif post_task_type == (task_type + '_create_task'): #else connecting to new task
                label = request.POST.get(task_type + '_task_label', '')
                print label
                if label and label != '':
                    new_tasks[task_type] = create_task(request.POST.get(task_type + '_create_task', None), label, spec_model)
                else: error = "New task requires a name"
        #Now we have the tasks for connecting in new_tasks[success/fail]. lets check that they are not none before connecting
        for task in new_tasks.values():
             if task is None or len(new_tasks) is not 2: error = "Must select valid tasks for success and fail branches"
        if not error: #No outstanding errors, lets connect
            from SpiffWorkflow.operators import Attrib, GreaterThan,\
                Equal, LessThan
            origin_task.set_data(min_score=0) #default required score
            origin_task.connect_if(GreaterThan(Attrib('score'), Attrib('min_score')),
                                new_tasks['success'])
            origin_task.connect_if(Equal(Attrib('score'), Attrib('min_score')),
                                new_tasks['success'])
            origin_task.connect_if(LessThan(Attrib('score'), Attrib('min_score')),
                                new_tasks['fail'])
            origin_task.connect(new_tasks['fail'])  # Default taskspec
            spec_model.save()
            return redirect('view_spec', spec_model.id)
    return render(request, 'spec_builder/taskforms/CheckTallyConnect.html', {
        'spec_model': spec_model,
        'origin_task': origin_task,
        'existing_tasks': {k: type(v).__name__ for k, v in spec_model.spec.task_specs.items()},
        'legal_tasks': {k: (v[0],v[1].__name__) for k, v in CONNECTABLE_TASKS.items()},
        'task_types': ['success', 'fail'],
        'error': error,
        'completed': completed
    })
    
def check_tally_dict(request, spec_model, task_spec):
    """controlller for dictionary editing of check_tally tasks (modification of field_entry_dict)"""
    fields = task_spec.get_data('task_data')['fields']
    min_score = task_spec.get_data('min_score')
    print min_score
    if request.method == "POST":
        if 'new_min_score' in request.POST:
            min_score = request.POST.get('min_score', '')
            task_spec.set_data(min_score = int(min_score) if (min_score != '') else 0) #convert score to int and save    
        elif 'new_field' in request.POST:
            name = request.POST.get('new_name', False)
            label = request.POST.get('new_label', False)
            score = request.POST.get('new_score', '')
            score = int(score) if (score != '') else 0 #convert score to int
            if 'new_mandatory' in request.POST: mandatory = True
            else: mandatory = False
            if name and label and len(name) is not 0 \
                and len(label) is not 0:
                fields[name] = {'label': label, 'mandatory': mandatory,
                                'type': 'checkbox', 'value': False, 'score': score}
        else:
            for field in fields:
                if field+'_delete' in request.POST:
                    del fields[field]
                    break
                label = request.POST.get(field+'_label', False)
                score = request.POST.get(field+'_score', '')
                score = int(score) if (score != '') else 0 #convert score to int
                if label and len(label) is not 0:
                    fields[field]['label'] = label
                if field+'_mandatory' in request.POST:
                    fields[field]['mandatory'] = True
                else: fields[field]['mandatory'] = False
                if score:
                    fields[field]['score'] = score
        task_spec.get_data('task_data')['fields'] = fields
        spec_model.save()

    return render(request, 'spec_builder/taskforms/CheckTallyDict.html', {
        'spec_model': spec_model,
        'task': task_spec,
        'fields': task_spec.get_data('task_data')['fields'],
        'field_types': field_types,
        'min_score': min_score
    })
    
    
CONNECTABLE_TASKS = {
    #name : ('Nice Name', spiff taskspec, connect method)
    'simple': ('Simple Task Node', taskspecs.Simple, None),
    'join': ('Blocking Join Node', taskspecs.Join, None),
    'choose_branch': ('Exclusive Branch', taskspecs.ExclusiveChoice, choose_branch_connect),
    'choose_branches': ('Multiple Branch', taskspecs.MultiChoice, choose_branches_connect),
    'check_tally': ('Checkbox Exclusive Branch', taskspecs.ExclusiveChoice, check_tally_connect)
    
}            
    
TASK_DICT_METHODS = {
    'file_upload': ('Upload a File', file_upload_dict),
    'accept_agreement': ('Accept an Agreement', accept_agreement_dict),
    'field_entry': ('Fill out Form Fields', field_entry_dict),
    'choose_branches': ('Multiple Branch', choose_branches_dict),
    'check_tally': ('Checkbox Branch', check_tally_dict),
}


                                  
            
    
 
