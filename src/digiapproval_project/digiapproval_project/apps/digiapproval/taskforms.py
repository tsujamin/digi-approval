from django import forms
from django.shortcuts import render
from . import models
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from exceptions import TypeError
import uuid

class AbstractForm(object):
    """
    Builds form template objects from the dictionaries stored in task_spec.task_data
    Fields:
        self.spiff_task: the task associated with the TaskForm object
        self.workflow_model: the model of the owning workflow
        self.task_model: the model storing the tasks data
        self.form: an instance of the form required by the task_model
        self.task_dict: equivalent to self.task_model.task
        self.actor: account which acts on this task (CUSTOMER/APPROVER)
    """
    
    @staticmethod
    def get_task_form(spiff_task, workflow_model):
        """ Finds the tasks form type and calls the correct initialiser.
            Marks the task complete and returns None if no task_data """
        if (spiff_task.task_spec.get_data('task_data') is not None) and ('form' in spiff_task.task_spec.get_data('task_data')):
            form_type = spiff_task.task_spec.get_data('task_data')['form']
            return form_classes[form_type](spiff_task, workflow_model)
        else:
            spiff_task.complete()
            workflow_model.save()
            return None
        
    
    def __init__(self, spiff_task, workflow_model,  *args, **kwargs):
        """Loads the saved task_model instance if it exists, 
        otherwise it saves a new one from the template in spiff_task.taskspec['task_data]"""
        self.spiff_task = spiff_task
        self.workflow_model = workflow_model
        if isinstance(spiff_task.id, dict):
            self.uuid = uuid.UUID(spiff_task.id['__uuid__'])
        else:
            self.uuid=spiff_task.id
              
        try: #task already has an associated task_model
            self.task_model = models.Task.objects.get(uuid=self.uuid)
        except: #need to make a new task_model object
            data_template = spiff_task.task_spec.get_data('task_data') #handles missing task data in get_task_form
            self.task_model = models.Task(workflow = workflow_model, task = data_template, uuid = self.uuid)
            self.task_model.save()
            workflow_model.save()
        self.task_dict = self.task_model.task
        self.actor = self.task_dict['actor']
        self.validate_task_data(self.task_dict)
    
    @staticmethod        
    def validate_task_data(task_data, *args, **kwargs): #handle in a better way
        """Validates that the task dict has the appropriate fields, IE: actor, form and fields"""
        from exceptions import AttributeError
        if task_data['form'] not in form_classes.keys():
            raise AttributeError("form of task must be key of form_classes")
        if  task_data['actor'] not in ['CUSTOMER', 'APPROVER']:
            raise AttributeError("actor of task must be customer or approver")
        if 'fields' in task_data:
            for field in task_data['fields'].values():
                if  'label' not in field or \
                    'type' not in field or \
                    'mandatory' not in field or \
                    type(field['mandatory']) is not bool or \
                    field['type'] not in field_types:
                        raise AttributeError("field must have label, legal type and boolean mandatory")
                        
    @staticmethod
    def make_task_dict(form, actor, *args, **kwargs):
        """Build valid task dictionary"""
        from exceptions import AttributeError
        if actor not in ['CUSTOMER', 'APPROVER']:
            raise AttributeError("actor of task must be customer or approver")
        elif form not in form_classes:
            raise AttributeError("form must be key of form_classes")
        return {'form': form, 
                'actor': actor, 
                'fields': {}, 
                'data': {}, 
                'options': {}
                }            
        
    def form_request(self, request):
        """Checks if user is permitted to view this form. if return is not none subclass must return its request.
            Doesn't currently return useful error messages on auth fail"""
        is_authenticated = request.user.is_authenticated()
        is_approver = request.user.id is self.workflow_model.approver.id
        is_customer_and_actor = (self.actor == 'CUSTOMER') and (request.user.customeraccount.id is self.workflow_model.customer.id)
        if not (is_authenticated and (is_approver or is_customer_and_actor)):
            return HttpResponseRedirect(reverse('applicant_home'))
    
    def complete_task(self, request):
        """ Sets current task as complete, saves the models and redirects to ndex or next task (if there is only one)
            Doesnt just get next task due to Join tasks being separate instances"""
        self.spiff_task.complete()
        self.task_model.save()
        self.workflow_model.save()
        waiting_tasks = self.workflow_model.get_ready_task_forms(actor=self.actor)
        if len(waiting_tasks) is 1:
            return waiting_tasks[0].form_request(request)
        else:
            return HttpResponseRedirect(reverse('view_workflow', args=(self.workflow_model.id,)))
        
class AcceptAgreement(AbstractForm):
    """Simple form which shows an agreement and has a boolean 'acceptance' field"""
    
    def __init__(self, spiff_task, workflow_model,  *args, **kwargs):
        super(AcceptAgreement, self).__init__(spiff_task, workflow_model,  *args, **kwargs)

    @staticmethod
    def validate_task_data(task_data):
        """Checks that the dictionary has acceptance field and agreement"""
        from exceptions import AttributeError
        AbstractForm.validate_task_data(task_data)
        if task_data['data']['agreement'] is None:
            raise AttributeError("data->agreement must exist")
        bool_field = task_data['fields']['acceptance']

    @staticmethod    
    def make_task_dict(mandatory, agreement, actor, *args, **kwargs):
        """Builds a valid taskdict. Fields given as *args parameter in form ()"""
        if 'label' in kwargs:
            label = kwargs['label']
        else:
            label = "Do you accept this agreement?"
        task_dict = AbstractForm.make_task_dict("accept_agreement", actor)
        task_dict['fields']['acceptance'] = {   'label': label, 'mandatory': mandatory, 
                                                'type': 'checkbox', 'value': False}
        task_dict['data']['agreement'] = agreement
        AcceptAgreement.validate_task_data(task_dict)
        return task_dict
        
    def form_request(self, request):
        response = super(AcceptAgreement, self).form_request(request)
        error = ""
        if response is not None: #invalid access
            return response
        if request.method == "POST":
            mandatory = self.task_dict['fields']['acceptance']['mandatory']
            checkbox_value = request.POST.get('checkbox_value', False) 
            if (mandatory and checkbox_value) or not mandatory: #success
                self.task_dict['fields']['acceptance']['value'] = checkbox_value
                return self.complete_task(request)
            error = "You must accept the agreement to continue"
        return render(request, 'digiapproval/taskforms/AcceptAgreement.html', { #default response
            'error': error,
            'task': self.spiff_task.get_name(),
            'agreement': self.task_dict['data']['agreement'],
            'checkbox_label': self.task_dict['fields']['acceptance']['label'],
            'checkbox_value': self.task_dict['fields']['acceptance']['value'],
        })
        
    def complete_task(self, request):
        """Perform post completion tasks"""
        return super(AcceptAgreement, self).complete_task(request)
    
class FieldEntry(AbstractForm):
    """Form for string field data entry. Could be modified to support other field types by changing the 
    'type' of the field (in dict)
    """
    def __init__(self, spiff_task, workflow_model,  *args, **kwargs):
        super(FieldEntry, self).__init__(spiff_task, workflow_model,  *args, **kwargs)

    @staticmethod
    def validate_task_data(task_data):
        """Checks validity of provided task dictionary. Just a passthrough as basic field 
        validation already performed by superclass"""
        AbstractForm.validate_task_data(task_data)
        
    @staticmethod    
    def make_task_dict(actor, *args, **kwargs):
        """Builds a task dictionary, accepts *args of (name, label, ftype, required). 
        Only text currently supported for ftype
        """
        task_dict = AbstractForm.make_task_dict("field_entry", actor)
        for (field_name, label, ftype, mandatory) in args:
            task_dict['fields'][field_name] = {   
                'label': label, 'mandatory': mandatory, 
                'type': ftype, 'value': False
            } 
        FieldEntry.validate_task_data(task_dict)
        return task_dict
        
    def form_request(self, request):
        response = super(FieldEntry, self).form_request(request)
        error = None
        render_dict = {}
        form_fields = self.task_dict['fields']
        
        if response is not None: return response #invalid access
        
        if request.method == "POST":
            for field in form_fields:
                value = request.POST.get(field, None)
                if value == '' and form_fields[field]['mandatory'] is True: #Failed to enter mandatory field
                    error = "\"" + str(form_fields[field]['label']) + "\" is a mandatory field."
                    break
                else: form_fields[field]['value'] = value
            if error is None: #Correctly filled out
                return self.complete_task(request)
        return render(request, 'digiapproval/taskforms/FieldEntry.html', { #default response
            'error': error,
            'task': self.spiff_task.get_name(),
            'form_fields': form_fields
        })
            
    def complete_task(self, request):
        """Perform post completion tasks"""
        return super(FieldEntry, self).complete_task(request)
                    
                
        
    
form_classes = {
    "accept_agreement": AcceptAgreement,
    "field_entry": FieldEntry  
}
field_types = [
    'checkbox',
    'text'
]
        
        
        
        
        
        
