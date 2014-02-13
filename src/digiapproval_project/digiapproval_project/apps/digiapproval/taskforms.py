from django.shortcuts import render
from . import models
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.template import Context, loader
from exceptions import TypeError, AttributeError
import uuid
from SpiffWorkflow.specs import ExclusiveChoice, MultiChoice


class AbstractForm(object):
    """
    Builds form template objects from the dictionaries stored in
    task_spec.task_data

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
        if (spiff_task.task_spec.get_data('task_data') is not None) and\
           ('form' in spiff_task.task_spec.get_data('task_data')):
            form_type = spiff_task.task_spec.get_data('task_data')['form']
            return form_classes[form_type](spiff_task, workflow_model)
        else:
            spiff_task.complete()
            workflow_model.save()
            return None

    @staticmethod
    def create_approval_wrapper(wf_spec, first_task, next_task, section, *args,
                                **kwargs):
        """Returns an APPROVER taskform which prompts the reviewer to accept
        the customers responses in the wrapped tasks. If they are unacceptable
        the task loops back."""

        review_task = ChooseBranch.create_exclusive_task(
            wf_spec,
            (section + ": Review"),
            (1, first_task),
            (2, next_task),
            )

        review_task.set_data(
            task_data=ChooseBranch.make_task_dict(
                'APPROVER',
                ('restart_section',
                 "Previous section needs to be re-completed", 1),
                ('continue',
                 "Previous section was completed acceptably", 2),
                task_info=kwargs.get('task_info', "")
                ))
        return review_task

    def __init__(self, spiff_task, workflow_model,  *args, **kwargs):
        """Loads the saved task_model instance if it exists, otherwise it saves
        a new one from the template in spiff_task.taskspec['task_data]"""
        self.spiff_task = spiff_task
        self.workflow_model = workflow_model
        if isinstance(spiff_task.id, dict):
            self.uuid = uuid.UUID(spiff_task.id['__uuid__'])
        else:
            self.uuid = spiff_task.id

        try:  # task already has an associated task_model
            self.task_model = models.Task.objects.get(uuid=self.uuid)
        except:  # need to make a new task_model object
            # handles missing task data in get_task_form
            data_template = spiff_task.task_spec.get_data('task_data')
            self.task_model = models.Task(workflow=workflow_model,
                                          task=data_template, uuid=self.uuid)
            self.task_model.save()
            workflow_model.save()
        self.task_dict = self.task_model.task
        self.actor = self.task_dict['actor']
        self.validate_task_data(self.task_dict)

    @staticmethod
    def validate_task_data(task_data, *args, **kwargs):
        # handle in a better way
        """Validates that the task dict has the appropriate fields, IE: actor,
        form and fields"""
        if task_data['form'] not in form_classes.keys():
            raise AttributeError("form of task must be key of form_classes")
        if task_data['actor'] not in ['CUSTOMER', 'APPROVER']:
            raise AttributeError("actor of task must be customer or approver")
        if 'task_info' not in task_data['data']:
            task_data['actor']['task_info'] = ""
        if 'fields' in task_data:
            for field in task_data['fields'].values():
                if 'label' not in field or \
                   'type' not in field or \
                   'mandatory' not in field or \
                   type(field['mandatory']) is not bool or \
                   field['type'] not in field_types:
                    raise AttributeError("field must have label, legal type " +
                                         "and boolean mandatory")

    @staticmethod
    def make_task_dict(form, actor, *args, **kwargs):
        """Build valid task dictionary, takes kwarg of task_info that is
        displayed alongside the task"""
        if actor not in ['CUSTOMER', 'APPROVER']:
            raise AttributeError("actor of task must be customer or approver")
        elif form not in form_classes:
            raise AttributeError("form must be key of form_classes")
        if 'task_info' in kwargs:
            task_info = kwargs['task_info']
        else:
            task_info = ""
        return {'form': form,
                'actor': actor,
                'fields': {},
                'data': {'task_info': task_info},
                'options': {}
                }

    def form_request(self, request):
        """Checks if user is permitted to view this form. if return is not none
            subclass must return its request.

            Doesn't currently return useful error messages on auth fail"""
        is_authenticated = request.user.is_authenticated()
        is_approver = request.user.id is self.workflow_model.approver.id
        is_customer_and_actor = (self.actor == 'CUSTOMER') and \
            hasattr(request.user, 'customeraccount') and \
            self.workflow_model.is_authorised_customer(
                request.user.customeraccount)

        if not (is_authenticated and (is_approver or is_customer_and_actor)):
            return HttpResponseRedirect(reverse('applicant_home'))
    
    def complete_task(self):
        """Sets current task as complete, saves the models, emails those involved"""
        self.spiff_task.complete()
        self.task_model.save()
        self.workflow_model.save()
        
        # send email. don't use the message class: we don't want it
        # displayed/stored
        sender = (self.workflow_model.approver if self.actor == 'APPROVER'
                  else self.workflow_model.customer.user)
        # construct a list of recipients
        recipients = self.workflow_model.get_involved_users_emails()
        recipients.remove(sender.email)

        # for now, send a very boring plain text only email via django.
        template = loader.get_template(
            'digiapproval/emails/completed_step.txt')
        context = Context({'taskform': self})
        # eww magic data - todo
        send_mail('DigiApproval: ' + self.workflow_model.spec.name,
                  template.render(context),
                  ('workflow-%s@digiactive.com.au' % self.workflow_model.uuid),
                  recipients, fail_silently=False)

        
    def complete_task_request(self, request):
        """Completes current task and redirects to index or next task (if there is only one).

        Doesn't just get next task due to Join tasks being separate instances."""
        # redirect
        
        self.complete_task()
        
        waiting_tasks = self.workflow_model.get_ready_task_forms(
            actor=self.actor)
        if len(waiting_tasks) is 1:
            return HttpResponseRedirect(
                reverse('view_task',
                        args=(waiting_tasks[0].workflow_model.id,
                              waiting_tasks[0].uuid,)))
        else:
            return HttpResponseRedirect(
                reverse('view_workflow', args=(self.workflow_model.id,)))


class AcceptAgreement(AbstractForm):
    """Simple form which shows an agreement and has a boolean 'acceptance'
    field"""

    def __init__(self, spiff_task, workflow_model,  *args, **kwargs):
        super(AcceptAgreement, self).__init__(spiff_task, workflow_model,
                                              *args, **kwargs)

    @staticmethod
    def validate_task_data(task_data):
        """Checks that the dictionary has acceptance field and agreement"""
        AbstractForm.validate_task_data(task_data)
        if task_data['data']['agreement'] is None:
            raise AttributeError("data->agreement must exist")
        if not 'acceptance' in task_data['fields']:
            raise AttributeError("must have an acceptance field")

    @staticmethod
    def make_task_dict(mandatory, agreement, actor, *args, **kwargs):
        """Builds a valid taskdict.
        Fields given as *args parameter in form ()"""
        if 'label' in kwargs:
            label = kwargs['label']
        else:
            label = "Do you accept this agreement?"
        task_dict = AbstractForm.make_task_dict("accept_agreement", actor,
                                                *args, **kwargs)
        task_dict['fields']['acceptance'] = {'label': label,
                                             'mandatory': mandatory,
                                             'type': 'checkbox',
                                             'value': False}
        task_dict['data']['agreement'] = agreement
        AcceptAgreement.validate_task_data(task_dict)
        return task_dict

    def form_request(self, request):
        response = super(AcceptAgreement, self).form_request(request)
        error = ""
        if response is not None:  # invalid access
            return response
        if request.method == "POST":
            mandatory = self.task_dict['fields']['acceptance']['mandatory']
            checkbox_value = request.POST.get('checkbox_value', None)
            if not mandatory:
                if checkbox_value is not None:
                    self.task_dict['fields']['acceptance']['value'] = True
                else:
                    self.task_dict['fields']['acceptance']['value'] = False
                return self.complete_task_request(request)
            elif mandatory and (checkbox_value is not None):
                self.task_dict['fields']['acceptance']['value'] = True
                return self.complete_task_request(request)
            error = "You must accept the agreement to continue"
        # default response
        return render(request, 'digiapproval/taskforms/AcceptAgreement.html', {
            'error': error,
            'task': self.spiff_task.get_name(),
            'agreement': self.task_dict['data']['agreement'],
            'checkbox_label': self.task_dict['fields']['acceptance']['label'],
            'checkbox_value': self.task_dict['fields']['acceptance']['value'],
            'task_info': self.task_dict['data']['task_info']
        })


class FieldEntry(AbstractForm):
    """Form for string field data entry. Could be modified to support other
    field types by changing the 'type' of the field (in dict)
    """
    def __init__(self, spiff_task, workflow_model,  *args, **kwargs):
        super(FieldEntry, self).__init__(spiff_task, workflow_model,
                                         *args, **kwargs)

    @staticmethod
    def validate_task_data(task_data):
        """Checks validity of provided task dictionary. Just a passthrough as
        basic field validation already performed by superclass"""
        AbstractForm.validate_task_data(task_data)

    @staticmethod
    def make_task_dict(actor, *args, **kwargs):
        """Builds a task dictionary.

        Accepts *args of (name, label, ftype, required).

        Only text currently supported for ftype
        """
        task_dict = AbstractForm.make_task_dict("field_entry", actor,
                                                *args, **kwargs)
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
        form_fields = self.task_dict['fields']

        if response is not None:
            # invalid access
            return response

        if request.method == "POST":
            for field in form_fields:
                value = request.POST.get(field, None)
                if (form_fields[field]['mandatory'] is True and
                        (value == '' or value is None)):

                    # Failed to enter mandatory field
                    error = ("\"" + str(form_fields[field]['label']) +
                             "\" is a mandatory field.")
                    break
                elif form_fields[field]['type'] == 'checkbox':
                    form_fields[field]['value'] = True
                else:
                    form_fields[field]['value'] = value
            if error is None:  # Correctly filled out
                return self.complete_task_request(request)
        # default response
        return render(request, 'digiapproval/taskforms/FieldEntry.html', {
            'error': error,
            'task': self.spiff_task.get_name(),
            'form_fields': form_fields,
            'task_info': self.task_dict['data']['task_info']
        })


class CheckTally(AbstractForm):
    """Displays a list of checkboxes with associated values. Selects a branch
    based on the total score of elected values"""

    def __init__(self, spiff_task, workflow_model,  *args, **kwargs):
        super(CheckTally, self).__init__(spiff_task, workflow_model,
                                         *args, **kwargs)
        if isinstance(spiff_task.task_spec, ExclusiveChoice) and \
                isinstance(spiff_task.task_spec.get_data('min_score'), int):
            spiff_task.set_data(
                min_score=spiff_task.task_spec.get_data('min_score'))
            spiff_task.set_data(score=0)
        else:
            raise TypeError("CheckTally requires an ExclusiveChoice task " +
                            "with score and min_score attributes")

    @staticmethod
    def validate_task_data(task_data):
        """Checks that the dictionary has integer branch score and scores for
        each field
        """
        AbstractForm.validate_task_data(task_data)
        for item in task_data['fields'].values():
            if item['type'] != 'checkbox' or \
                    not isinstance(item['score'], int):
                raise AttributeError("fields must have score and be checkbox")

    @staticmethod
    def make_task_dict(actor, *args, **kwargs):
        """Builds a task dictionary.

        Accepts *args of (name, label, mandatory, score).

        Only text currently supported for ftype.
        """
        task_dict = AbstractForm.make_task_dict("check_tally", actor, *args,
                                                **kwargs)
        for (field_name, label, mandatory, score) in args:
            task_dict['fields'][field_name] = {
                'label': label, 'mandatory': mandatory,
                'type': 'checkbox', 'value': False, 'score': score
            }
        CheckTally.validate_task_data(task_dict)
        return task_dict

    def form_request(self, request):
        response = super(CheckTally, self).form_request(request)
        error = None
        form_fields = self.task_dict['fields']

        if response is not None:
            # invalid access
            return response

        if request.method == "POST":
            current_score = 0
            for field in form_fields:
                value = request.POST.get(field, None)
                # Failed to enter mandatory field
                if value is None and form_fields[field]['mandatory'] is True:
                    error = ("\"" + str(form_fields[field]['label']) +
                             "\" is a mandatory field.")
                    break
                elif value is not None:
                    form_fields[field]['value'] = True
                    current_score += form_fields[field]['score']
            if error is None:
                # Correctly filled out
                self.spiff_task.set_data(score=current_score)
                return self.complete_task_request(request)
        # default response
        return render(request, 'digiapproval/taskforms/CheckTally.html', {
            'error': error,
            'task': self.spiff_task.get_name(),
            'form_fields': form_fields,
            'task_info': self.task_dict['data']['task_info']
        })

    @staticmethod
    def create_exclusive_task(spec, name, min_score, success, fail, *args,
                              **kwargs):
        """Build an ExclsiveChoice task for attachment to this task
        form. Requires a minimal pass score, success and fail branches.
        """
        from SpiffWorkflow.operators import Attrib, GreaterThan,\
            Equal, LessThan
        ret_task = ExclusiveChoice(spec, name)
        ret_task.set_data(min_score=min_score)
        ret_task.connect_if(GreaterThan(Attrib('score'), Attrib('min_score')),
                            success)
        ret_task.connect_if(Equal(Attrib('score'), Attrib('min_score')),
                            success)
        ret_task.connect_if(LessThan(Attrib('score'), Attrib('min_score')),
                            fail)
        ret_task.connect(success)  # Default taskspec
        return ret_task


class ChooseBranch(AbstractForm):
    """A small example of a task form. TaskForms based on this template must be
    added to the form_classes tuple array at the bottom of taskforms.py"""

    def __init__(self, spiff_task, workflow_model, *args, **kwargs):
        """Task form initialisation and validation"""
        super(ChooseBranch, self).__init__(spiff_task, workflow_model,
                                           *args, **kwargs)
        if not isinstance(spiff_task.task_spec, ExclusiveChoice):
            raise TypeError("CheckTally requires an ExclusiveChoice task")

    @staticmethod
    def validate_task_data(task_data):
        """Validates that provided task_data dict is of valid construction,
        throws AttributeErrors"""
        AbstractForm.validate_task_data(task_data)
        for field in task_data['fields']:
            if not hasattr(field, 'number') or field['type'] != 'radio':
                AttributeError("fields must have number and be of type radio")

    @staticmethod
    def make_task_dict(actor, *args, **kwargs):
        """Constructs a task_dict for this taskform using provided args (name,
        label, number), Actor must be CUSTOMER or APPROVER"""
        task_dict = AbstractForm.make_task_dict("choose_branch", actor, *args,
                                                **kwargs)
        for (name, label, number) in args:
            task_dict['fields'][name] = {
                'label': label, 'mandatory': False,
                'type': 'radio', 'value': False, 'number': number
            }
        ChooseBranch.validate_task_data(task_dict)
        return task_dict

    def form_request(self, request):
        """Controller for this task form, handles post and checks validity
        before completing task"""
        # Check authorisation
        response = super(ChooseBranch, self).form_request(request)
        if response is not None:
            # invalid access
            return response
        error = None
        form_fields = self.task_dict['fields']
        if request.method == "POST":
            value = request.POST.get('selection', None)
            if value is not None and value in form_fields:
                form_fields[value]['value'] = True
                self.spiff_task.set_data(
                    selection=form_fields[value]['number'])
                return self.complete_task_request(request)
            else:
                error = "Invalid Selection"
        # default response, returns related template with current fields
        return render(request, 'digiapproval/taskforms/ChooseBranch.html', {
            'error': error,
            'task': self.spiff_task.get_name(),
            'form_fields': form_fields,
            'task_info': self.task_dict['data']['task_info']
        })

    @staticmethod
    def create_exclusive_task(spec, name, *args, **kwargs):
        """Build an ExclsiveChoice task for attachment to this task
        form. requires *args of (choice_no, taskspec)
        """
        from SpiffWorkflow.operators import Attrib, Equal
        ret_task = ExclusiveChoice(spec, name)
        for (number, taskspec) in args:
            ret_task.connect_if(Equal(Attrib('selection'), number), taskspec)
        (_, default_task) = args[0]  # First task is default
        ret_task.connect(default_task)
        return ret_task


class ChooseBranches(AbstractForm):
    """A small example of a task form. TaskForms based on this template must be
    added to the form_classes tuple array at the bottom of taskforms.py"""

    def __init__(self, spiff_task, workflow_model, *args, **kwargs):
        """Task form initialisation and validation"""
        super(ChooseBranches, self).__init__(spiff_task, workflow_model, *args,
                                             **kwargs)
        if isinstance(spiff_task.task_spec, MultiChoice):
            for field in self.task_dict['fields']:
                data_field = ("task" +
                              str(self.task_dict['fields'][field]['number']))
                if not hasattr(self.spiff_task.data, data_field):
                    # init fields
                    self.spiff_task.data[data_field] = False
                self.task_model.save()
        else:
            raise TypeError("CheckTally requires an MultiChoice task")

    @staticmethod
    def validate_task_data(task_data):
        """Validates that provided task_data dict is of valid construction,
        throws AttributeErrors"""
        AbstractForm.validate_task_data(task_data)
        for field in task_data['fields'].values():
            if not 'number' in field or \
                    field['type'] != 'checkbox':
                print field
                raise AttributeError("fields must have number and be of type" +
                                     " checkbox")
        if not 'minimum_choices' in task_data['options'] or \
                not isinstance(task_data['options']['minimum_choices'], int):
            raise AttributeError("must have an integer minimum_choices option")

    @staticmethod
    def make_task_dict(actor, minimum_choices, *args, **kwargs):
        """Constructs a task_dict for this taskform using provided args (name,
        label, number), Actor must be CUSTOMER or APPROVER"""
        task_dict = AbstractForm.make_task_dict("choose_branches", actor,
                                                *args, **kwargs)
        for (name, label, number) in args:
            task_dict['fields'][name] = {
                'label': label, 'mandatory': False,
                'type': 'checkbox', 'value': False, 'number': number
            }
        task_dict['options']['minimum_choices'] = minimum_choices
        ChooseBranches.validate_task_data(task_dict)
        return task_dict

    def form_request(self, request):
        """Controller for this task form, handles post and checks validity
        before completing task"""
        # Check authorisation
        response = super(ChooseBranches, self).form_request(request)
        if response is not None:
            # invalid access
            return response

        form_fields = self.task_dict['fields']
        error = None
        count = 0
        if request.method == "POST":
            for field in form_fields:
                print request.POST
                value = request.POST.get(field, None)
                if value is not None:
                    form_fields[field]['value'] = True
                    data_field = "task" + str(form_fields[field]['number'])
                    self.spiff_task.data[data_field] = True
                    count += 1
            if count >= self.task_dict['options']['minimum_choices']:
                return self.complete_task_request(request)
            else:
                error = ("Please select at least " +
                         str(self.task_dict['options']['minimum_choices']) +
                         " option(s)")
        # default response, returns related template with current fields
        return render(request, 'digiapproval/taskforms/ChooseBranches.html', {
            'error': error,
            'task': self.spiff_task.get_name(),
            'form_fields': form_fields,
            'task_info': self.task_dict['data']['task_info']
        })

    @staticmethod
    def create_multichoice_task(spec, name, *args, **kwargs):
        """Build an ExclsiveChoice task for attachment to this task
        form. requires *args of (choice_no, taskspec)
        """
        from SpiffWorkflow.operators import Attrib, Equal
        ret_task = MultiChoice(spec, name)
        for (number, taskspec) in args:
            data_field = "task" + str(number)
            ret_task.connect_if(Equal(Attrib(data_field), True), taskspec)
        return ret_task


class FileUpload(AbstractForm):
    """A small example of a task form.

    TaskForms based on this template must be added to the form_classes tuple
    array at the bottom of taskforms.py"""

    def __init__(self, spiff_task, workflow_model, *args, **kwargs):
        """Task form initialisation and validation"""
        super(FileUpload, self).__init__(spiff_task, workflow_model, *args,
                                         **kwargs)
        # Task specific init/validation here

    @staticmethod
    def validate_task_data(task_data):
        """Validates that provided task_data dict is of valid construction,
        throws AttributeErrors"""
        AbstractForm.validate_task_data(task_data)
        if (not hasattr(task_data['fields'], 'file') and
                hasattr(task_data['fields'], 'file_name')):
            raise AttributeError("Needs file field")

    @staticmethod
    def make_task_dict(mandatory, actor, *args, **kwargs):
        """Constructs a task_dict for this taskform using provided params"""
        task_dict = AbstractForm.make_task_dict("file_upload", actor, *args,
                                                **kwargs)
        task_dict['fields']['file_name'] = {
            'label': 'Name of File: ', 'mandatory': mandatory,
            'type': 'text', 'value': "",
        }
        task_dict['fields']['file'] = {
            'label': 'Upload File:', 'mandatory': mandatory,
            'type': 'file', 'value': None,
        }
        FileUpload.validate_task_data(task_dict)
        return task_dict

    def form_request(self, request):
        """Controller for this task form, handles post and checks validity
        before completing task"""
        # Check authorisation
        response = super(FileUpload, self).form_request(request)
        if response is not None:
            # invalid access
            return response
        error = None
        
        if request.method == "POST":
            file = request.FILES.get('file', None)
            file_name = request.POST.get('file_name', None)
            #save filename in field for re-render
            if file_name and file_name != "" :
                self.task_dict['fields']['file_name']['value'] = file_name
            # Check validity of posted data
            if file is None and self.task_dict['fields']['file']['mandatory']:
                error = "Uploading a file is mandatory"
            elif file_name == "" and file is not None:
                error = "Uploaded files require a label"
            else:  # place filevalue in task_dict
                file_model = models.UserFile(_file=file, name=file_name)
                file_model.save()
                self.task_dict['fields']['file']['value'] = file_model.id
                return self.complete_task_request(request)
        # default response, returns related template with current fields
        return render(request, 'digiapproval/taskforms/FileUpload.html', {
            'error': error,
            'task': self.spiff_task.get_name(),
            'form_fields': self.task_dict['fields'],
            'task_info': self.task_dict['data']['task_info']
        })


class Subworkflow(AbstractForm):
    """Allows workflow to be embedded as a task in a different workflow"""
    
    def __init__(self, spiff_task, workflow_model, *args, **kwargs):
        """Task form initialisation and validation"""
        super(Subworkflow, self).__init__(spiff_task, workflow_model, *args, **kwargs)
        
        # Create the sub-Workflow if it's not already created
        if 'workflow_id' not in self.task_dict['data']:
            workflowspec = models.WorkflowSpec.objects.get(id=self.task_dict['data']['workflowspec_id'])
            workflow = workflowspec.start_workflow(self.workflow_model.customer)
            workflow.parent_workflow = self.workflow_model
            workflow.parent_task = self.task_model
            workflow.save()
            self.task_dict['data']['workflow_id'] = workflow.id
            self.task_model.save()
            self.workflow_model.save()
        
        # Check if the sub-Workflow has completed, and if so, complete the Subworkflow task
        # TODO this technically doesn't trigger when the sub-Workflow completes, it triggers when
        # the user looks at things again, causing the Subworkflow taskform to be instantiated
        workflow = models.Workflow.objects.get(pk=self.task_dict['data']['workflow_id'])
        if workflow.completed:
            self.complete_task()

        
    @staticmethod
    def validate_task_data(task_data):
        """Validates that provided task_data dict is of valid construction, throws AttributeErrors"""    
        AbstractForm.validate_task_data(task_data)
        #Test taskform specific fields here
        
    @staticmethod    
    def make_task_dict(actor, workflowspec_id, *args, **kwargs):
        """Constructs a task_dict for this taskform using provided params"""
        task_dict = AbstractForm.make_task_dict("subworkflow", actor, *args, **kwargs)
        task_dict['data']['workflowspec_id'] = workflowspec_id
        
        #Add task specific forms to task_dict
        Subworkflow.validate_task_data(task_dict)
        return task_dict
        
        
    def form_request(self, request):
        """Controller for this task form, handles post and checks validity before completing task
        
        Redirects user to the sub-Workflow"""
        response = super(Subworkflow, self).form_request(request) #Check authorisation
        if response is not None: return response #invalid access
        
        return HttpResponseRedirect(reverse('view_workflow', args=(self.task_dict['data']['workflow_id'],)))
    

    def complete_task_request(self, request):
        """Subworkflows shouldn't be completed manually - raise exception"""
        raise Exception("complete_task_request() called on Subworkflow")


class ExampleTaskForm(AbstractForm):
    """A small example of a task form.

    TaskForms based on this template must be added to the form_classes tuple
    array at the bottom of taskforms.py"""

    def __init__(self, spiff_task, workflow_model, *args, **kwargs):
        """Task form initialisation and validation"""
        super(ExampleTaskForm, self).__init__(spiff_task, workflow_model,
                                              *args, **kwargs)
        #Task specific init/validation here

    @staticmethod
    def validate_task_data(task_data):
        """Validates that provided task_data dict is of valid construction,
        throws AttributeErrors"""
        AbstractForm.validate_task_data(task_data)
        #Test taskform specific fields here

    @staticmethod
    def make_task_dict(actor, *args, **kwargs):
        """Constructs a task_dict for this taskform using provided params"""
        task_dict = AbstractForm.make_task_dict("example_task_form", actor,
                                                *args, **kwargs)
        #Add task specific forms to task_dict
        ExampleTaskForm.validate_task_data(task_dict)
        return task_dict

    def form_request(self, request):
        """Controller for this task form, handles post and checks validity
        before completing task"""
        # Check authorisation
        response = super(ExampleTaskForm, self).form_request(request)
        if response is not None:
            # invalid access
            return response
        error = None

        if request.method == "POST":
            for field in self.task_dict['fields']:
                value = request.POST.get(field, None)

                # Define validity for POSTed data
                valid = True and hasattr(self.task_dict['fields'], field)
                # Check for invalidity or missing mandatory field
                if not valid or \
                    (value is None and
                     self.task_dict['fields'][field]['mandatory']):
                    error = "Error text"
                else:  # place value in task_dict
                    self.task_dict['fields'][field]['value'] = value
            if error is None:
                # All field data was valid, now complete the task
                return self.complete_task_request(request)
        # default response, returns related template with current fields
        return render(request, 'digiapproval/taskforms/ExampleTaskForm.html', {
            'error': error,
            'task': self.spiff_task.get_name(),
            'form_fields': self.task_dict['fields'],
            'task_info': self.task_dict['data']['task_info']
        })

form_classes = {
    "accept_agreement": AcceptAgreement,
    "field_entry": FieldEntry,
    "check_tally": CheckTally,
    "choose_branch": ChooseBranch,
    "choose_branches": ChooseBranches,
    "file_upload": FileUpload,
    "subworkflow": Subworkflow,
}

field_types = [
    'checkbox',
    'text',
    'radio',
    'file',
]
