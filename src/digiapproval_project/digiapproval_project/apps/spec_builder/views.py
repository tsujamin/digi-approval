from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from digiapproval_project.apps.digiapproval.auth_decorators import login_required_super
from digiapproval_project.apps.digiapproval import models as approval_models

def index(request):
    raise NotImplementedError

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
            raise NotImplementedError
    wf_spec_ordered = {} #{owner: [specs],...}
    for spec in approval_models.WorkflowSpec.objects.all():
        if spec.owner.name not in wf_spec_ordered: wf_spec_ordered[spec.owner.name] = []
        wf_spec_ordered[spec.owner.name].append(spec)
        
    return render(request, 'spec_builder/builder_home.html', {
        'spec_list': wf_spec_ordered,
    })
            
    
 
