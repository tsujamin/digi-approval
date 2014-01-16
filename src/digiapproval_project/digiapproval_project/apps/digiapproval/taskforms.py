from . import models

class AbstractForm():
    """
    Builds form template objects from the dictionaries stored in task_spec.task_data
    Fields:
        self.spiff_task: the task associated with the TaskForm object
        self.workflow_model: the model of the owning workflow
        self.task_model: the model storing the tasks data
        self.form: an instance of the form required by the task_model
    """
    
    @staticmethod
    def get_task_form(spiff_task, workflow_model):
        """ Finds the tasks form type and calls the correct initialiser.
            Marks the task complete and returns None if no task_data """
        #try:
        form_type = spiff_task.task_spec.get_data('task_data')['form']
        return form_classes[form_type](spiff_task, workflow_model)
        #except:
        #    spiff_task.complete()
        #    return None
        
    
    def __init__(self, spiff_task, workflow_model,  *args, **kargs):
        """Loads the saved task_model instance if it exists, 
        otherwise it saves a new one from the template in spiff_task.taskspec['task_data]"""
        self.spiff_task = spiff_task
        self.workflow_model = workflow_model
        try: #task already has an associated task_model
            model_id = spiff_task.get_data('model_id')
            self.task_model = models.Task.objects.get(id=model_id)
        except: #need to make a new task_model object
            data_template = spiff_task.task_spec.get_data('task_data') #Doesnt handle missing task_data
            self.task_model = models.Task(workflow = workflow_model, task = data_template) 
            self.task_model.save()
            spiff_task.set_data(model_id = task_model.id) 
            workflow_model.save()
        self.validate_task_data(task_model.task)
    
    @staticmethod        
    def validate_task_data(task_data, *args, **kargs): #handle in a better way
        """Validates that the task dict has the appropriate fields, IE: actor, form and fields"""
        from exceptions import AttributeError
        if task_data['form'] not in form_classes.keys():
            raise AttributeError("form of task must be key of form_classes")
        if  task_data['actor'] not in ['customer', 'approver']:
            raise AttributeError("actor of task must be customer or approver")
        if 'fields' in task_data:
            for field in task_data['fields'].values():
                if  'label' not in field or \
                    'type' not in field or \
                    'mandatory' not in field or \
                    type(field['mandatory']) is not bool:
                        print field['type']
                        raise AttributeError("field must have label, type and mandatory")
                        
    @staticmethod
    def make_task_dict(form, actor, *args, **kargs):
        """Build valid task dictionary"""
        from exceptions import AttributeError
        if actor not in ['customer', 'approver']:
            raise AttributeError("actor of task must be customer or approver")
        elif form not in form_classes:
            raise AttributeError("form must be key of form_classes")
        return {'form': form, 
                'actor': actor, 
                'fields': {}, 
                'data': {}, 
                'options': {}
                }            
        
    def handle_httpy_stuff(*args, **kargs):
        pass

        
class AcceptAgreement(AbstractForm):
    """
    Simple form which shows an agreement and has a boolean 'acceptance' field
    """
    def __init__(self, spiff_task, workflow_model,  *args, **kargs):
        super(AbstractForm, self).__init__(spiff_task, workflow_model,  *args, **kargs)
    
    @staticmethod
    def validate_task_data(task_data):
        """Checks that the dictionary has acceptance field and agreement"""
        from exceptions import AttributeError
        AbstractForm.validate_task_data(task_data)
        if task_data['data']['agreement'] is None:
            raise AttributeError("data->agreement must exist")
        bool_field = task_data['fields']['acceptance']
        
    @staticmethod    
    def make_task_dict(label, mandatory, agreement, actor):
        """Builds a task dictionary"""
        task_dict = AbstractForm.make_task_dict("accept_agreement", actor)
        task_dict['fields']['acceptance'] = {   'label': label, 'mandatory': mandatory, 
                                                'type': 'checkbox', 'value': False}
        task_dict['data']['agreement'] = agreement
        AcceptAgreement.validate_task_data(task_dict)
        return task_dict
        
    
form_classes = {
    "accept_agreement": AcceptAgreement  
}
        
        
        
        
        
        