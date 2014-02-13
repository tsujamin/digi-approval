from __future__ import absolute_import

import uuid

from django.db import models
from django.contrib.auth.models import Group, User
from django.core.mail import send_mail
from django.template import Context, loader
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

from registration.signals import user_registered
from jsonfield import JSONField

from .fields import WorkflowField, WorkflowSpecField

class UserFile(models.Model):
    VIRUS_STATUS_CHOICES = (
        ('UNSCANNED', "Unscanned, not queued for scanning."),
        ('PENDING', "Queued for scanning, scan pending."),
        ('THREATFOUND', "Scanned, a threat was found."),
        ('CLEAN', "Scanned, no threat found."),
        ('ERROR', "An error occured during virus scanning.")
        )

    name = models.CharField(max_length=255)
    _file = models.FileField(upload_to="userfiles")
    virus_status = models.CharField(max_length=16,
                                    choices=VIRUS_STATUS_CHOICES,
                                    default='UNSCANNED')

    def save(self, *args, **kwargs):
        """Save the user file, queueing up the virus scan if the file
        is UNSCANNED."""

        # if necessary, scan and save PENDING status.
        if self.virus_status == 'UNSCANNED':
            from .tasks import virus_scan
            self.virus_status = 'PENDING'
            super(UserFile, self).save(*args, **kwargs)
            # scan *after* we set the PENDING state to avoid a race
            # condition were an actual status could be overwritten
            virus_scan.delay(self.pk)
        else:
            # otherwise just save
            super(UserFile, self).save(*args, **kwargs)

    @property
    def file(self):
        """Return the file only if it is safe to do so, otherwise
        return None."""

        if not self.virus_status == 'CLEAN':
            return None

        return self._file


class CustomerAccount(models.Model):
    """ End user model. Can either be Customer (single user) or Organisation
    (User with sub accounts).

    Related accounts of Organisation must be a list of users. Organisations can
    add users to this list.

    Related accounts of User are the organisations it is a part of and whose
    workflows it can use."""

    ACCOUNT_TYPE_CHOICES = (
        ('CUSTOMER', 'Customer account'),
        ('ORGANISATION', 'Organisation account'),
    )

    user = models.OneToOneField(User)
    account_type = models.CharField(max_length=16,
                                    choices=ACCOUNT_TYPE_CHOICES,
                                    default='CUSTOMER')
    # FIXME: does this allow for multiple levels of parent accounts?
    parent_accounts = models.ManyToManyField('self',
                                             symmetrical=False,
                                             related_name='sub_accounts',
                                             blank=True, null=True)

    def get_own_workflows(self, *args, **kwargs):
        """Get workflows owned by this user, takes **kwarg of ['completed'] as
        filter, otherwise returns all"""
        try:
            if 'completed' in kwargs:
                result = list(self.workflow_customer.filter(
                    completed=bool(kwargs['completed'])))
            else:
                result = list(self.workflow_customer.all())
        except ObjectDoesNotExist:
            result = []
        return result

    def get_all_workflows(self, *args, **kwargs):
        """Gets workflows of self and parent accounts, takes **kwarg of
        ['completed'] as filter, otherwise returns all"""
        workflow_list = self.get_own_workflows(*args, **kwargs)
        for parent in self.parent_accounts.all():
            workflow_list.extend(parent.get_own_workflows(*args, **kwargs))
        return workflow_list

    def save(self, *args, **kwargs):
        # DOESN'T VALIDATE PROPERLY ON THE FIRST DJANGO-ADMIN SAVE, DOES AFTER
        # THAT. MANY TO MANY NOT SAVING? TODO FIXME
        """Saves related auth.User object. Checks types of related accounts for
        legality (ie customer doesnt have sub accounts)"""
        from exceptions import ValueError
        if self.id:  # already saved
            if self.account_type == 'CUSTOMER':
                if self.sub_accounts.count() != 0:
                    raise ValueError("Customers cannot have sub accounts")
                if self.parent_accounts.filter(
                        account_type='CUSTOMER').count() != 0:
                    raise ValueError("Parent Accounts must be Organisations")
            elif self.account_type == 'ORGANISATION':
                if self.parent_accounts.count() != 0:
                    raise ValueError(
                        "Organisations cannot have parent accounts")
                if self.sub_accounts.filter(
                        account_type='ORGANISATION').count() != 0:
                    raise ValueError("Sub accounts must be customers")
        try:
            # Save related user, exceptions will be emitted in
            # CustomerAccount.save()
            self.user.save()
        finally:
            super(CustomerAccount, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.account_type + ": " + self.user.username


class WorkflowSpec(models.Model):
    name = models.CharField(max_length="64")
    description = models.TextField(blank=True)

    # A WorkflowSpec must have an owner group, but it may not have a delegators
    # or approvers group - this is to help with initial development/setup of
    # the WfS
    owner = models.ForeignKey(Group, related_name='workflowspecs_owner')
    delegators = models.ForeignKey(Group,
                                   related_name='workflowspecs_delegators',
                                   null=True, blank=True, default=None)
    approvers = models.ForeignKey(Group,
                                  related_name='workflowspecs_approvers',
                                  null=True, blank=True, default=None)

    public = models.BooleanField(default=False)
    toplevel = models.BooleanField(default=True)

    # disable editing: it doesn't render properly in Django admin, and besides
    # we have no need to modify it in the admin interface anyway -- AJD
    spec = WorkflowSpecField(editable=False)

    def start_workflow(self, customer):
        """Returns a workflow object derived from self's spec"""
        from SpiffWorkflow import Workflow as SWorkflow
        workflow = Workflow(customer=customer,
                            spec=self,
                            workflow=SWorkflow(self.spec))
        # complete the empty start task
        workflow.workflow.complete_next()
        return workflow

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.owner.name)


class Workflow(models.Model):
    STATE_CHOICES = [
        ('STARTED', "The workflow has been started"),
        ('CANCELLED', "The workflow was canceled"),
        ('APPROVED', "The workflow was approved"),
        ('DENIED', "The workflow was denied approval")
        ]

    customer = models.ForeignKey(CustomerAccount,
                                 related_name='workflow_customer')
    approver = models.ForeignKey(User, related_name='workflow_approver')
    # disable editable: it doesn't render properly in Django admin, and besides
    # we have no need to modify it in the admin interface anyway -- AJD
    workflow = WorkflowField(editable=False)
    completed = models.BooleanField(default=False)
    state = models.CharField(max_length=10,
                             choices=STATE_CHOICES,
                             default='STARTED')
    spec = models.ForeignKey(WorkflowSpec)
    # for reference in emails
    # TODO FIXME: are we using uuid.hex? no hyphens!
    uuid = models.CharField(max_length=36, editable=False,
                            default=lambda: uuid.uuid4().hex)
    
    # Parent information for subworkflows
    parent_workflow = models.ForeignKey('Workflow', null=True, blank=True, default=None,
                                        related_name='subworkflows')
    parent_task = models.ForeignKey('Task', null=True, blank=True, default=None,
                                    related_name='subworkflows')
    
    # Descriptive information
    label = models.CharField(max_length=50, default="Untitled Application")

    def assign_approver(self):
        """Finds the least busy approver (in the approvers group of the
        Workflows spec), returns and assigns it to the workflow"""
        if self.spec is None:
            raise UnboundLocalError("Workflow has no assigned WorkflowSpec")
        active_approvers = User.objects.filter(groups=self.spec.approvers,
                                               is_active=True)
        #Generates a dict of {Approver: no. current workflows}
        approver_wf_count = dict(
            map(lambda x: (x['approver'], x['approver__count']),
                Workflow.objects.filter(completed=False,
                                        spec__owner=self.spec.approvers)
                .values('approver').annotate(models.Count('approver'))
                )
            )
        #Find unassigned approver
        for approver in active_approvers:
            if approver.id not in approver_wf_count.keys():
                self.approver = approver
                return approver
        #Find least busy approver
        least_wf_approver = min(approver_wf_count, key=approver_wf_count.get)
        approver = User.objects.get(id=least_wf_approver)
        self.approver = approver
        return approver

    def save(self, *args, **kwargs):
        """Auto assigns approver if none provided"""
        from django.core.exceptions import ObjectDoesNotExist
        try:
            self.approver
        except ObjectDoesNotExist:
            self.assign_approver()
        if self.workflow.is_completed() and self.completed is False:
            self.completed = True
        
        super(Workflow, self).save(*args, **kwargs)

    def get_ready_task_forms(self, **kwargs):
        """ Iterates to find ready tasks and returns them as a list of
        task_forms, results can be filtered by optional argument 'actor'"""
        from .taskforms import AbstractForm as Form
        ready_forms = []
        for task in self.workflow.get_tasks():
            form = None
            if task.state is task.READY:
                form = Form.get_task_form(task, self)
            # Check that task had form before adding to list
            if form is not None:
                ready_forms.append(form)
        if 'actor' in kwargs:  # filter for requested actor
            ready_forms = [form for form in ready_forms
                           if form.actor == kwargs['actor']]
        return ready_forms

    def get_involved_users(self):
        """Returns a list of users: everyone involved in the workflow - the
        customer (as a User, not a CustomerAccount), the approver, and if the
        customer is an organisation, all the associated users (as Users, not
        CustomerAccounts)"""
        users = [self.customer.user, self.approver]
        users.extend(map(lambda custacc: (custacc.user),
                         self.customer.sub_accounts.all()))
        return users

    def get_involved_users_emails(self):
        """Returns a list of emails addresses of everyone involved in the
        workflow - the customer's email, the approver's email, and if the
        customer is an organisation, all the associated users' emails"""
        return [user.email for user in self.get_involved_users()]

    def is_authorised_customer(self, customer_account):
        """Checks if customer is authorised to modify workflow"""
        if not (customer_account == self.customer or
                customer_account in self.customer.sub_accounts.all()):
            return False
        return True

    def actor_type(self, user):
        """Identifies if the user account is the CUSTOMER or APPROVER
        of this workflow. Returns None if the user is neither."""

        try:
            customer = user.customeraccount
            actor = 'CUSTOMER'
            # FIXME: this doesn't cope with multiple layers of parent account -
            # but we should probably remove those multiple layers
            if customer != self.customer and \
                    self.customer not in self.customer.parent_accounts.all():
                return None
        except:
            actor = 'APPROVER'
            if user != self.approver:
                return None
        return actor

    def change_state_by_user(self, new_state='', user=None):
        """Can the user change this workflow's state to new_state? If so,
        make the change, otherwise raise an exception to say why not.

        Raises PermissionDenied errors if the user lacks the permissions.
        Raises ValueError if the change requested is invalid (e.g. restarting
        an abandoned workflow, invalid state)."""

        states = map(lambda (choice, _): (choice), Workflow.STATE_CHOICES)
        if new_state not in states:
            raise ValueError(("Attempted to change into state '%s', which is" +
                             " not a valid state.") % new_state)

        actor = self.actor_type(user)
        if actor is None:
            raise PermissionDenied

        if actor == 'CUSTOMER' and new_state != 'CANCELLED':
            raise PermissionDenied

        # A workflow cannot be uncancelled.
        if self.state not in ['DENIED', 'CANCELLED']:
            self.state = new_state  # assign new state
            if self.state == 'STARTED':
                self.completed = False
            elif self.state in ['DENIED', 'CANCELLED']:
                self.workflow.cancel()
                self.completed = True
            else:
                self.completed = True
        else:
            raise ValueError("A cancelled or denied workflow cannot be" +
                             " restarted.")
        self.save()

    def __unicode__(self):
        return u'%s (%s)' % (self.customer.user.username, self.spec.name)


class Task(models.Model):
    workflow = models.ForeignKey(Workflow)
    task = JSONField()
    uuid = models.CharField(max_length="36")


class Message(models.Model):
    workflow = models.ForeignKey(Workflow)
    sender = models.ForeignKey(User)
    posted = models.DateTimeField(auto_now=True)
    message = models.TextField()
    _sent = models.BooleanField(default=False, editable=False)
    last_read_by = models.ManyToManyField(User,
                                          related_name="last_read")

    def save(self, *args, **kwargs):
        """Sends an email to other people involved in the workflow if it hasn't
        been sent already."""

        if not self._sent:
            # construct a list of recipients
            recipients = self.workflow.get_involved_users_emails()
            recipients.remove(self.sender.email)

            # for now, send a very boring plain text only email
            template = loader.get_template('digiapproval/emails/message.txt')
            context = Context({'message': self})
            # eww magic data
            # todo break this out to celery.
            send_mail('DigiApproval: ' + self.workflow.spec.name,
                      template.render(context),
                      'workflow-' + self.workflow.uuid + '@digiactive.com.au',
                      recipients, fail_silently=False)

            self._sent = True
        super(Message, self).save(*args, **kwargs)

    @staticmethod
    def get_unread_messages(workflow, user):
        """Gets the list of messages the user has not yet read
        """
        last_read_message = user.last_read.filter(workflow=workflow)
        if last_read_message.count() is 1:
            message_id = last_read_message.first().id
        elif last_read_message.count() is 0:
            message_id = 0
        else:
            raise ValueError("Only one workflow/user combination should exist \
in last_read_by")
        return workflow.message_set.filter(id__gt=message_id)

    @staticmethod
    def mark_all_read(workflow, user):
        """Finds the "last read message" for the workflow/user combination and
        updates it to the last posted message.
        """
        last_read_message = user.last_read.filter(workflow=workflow)
        # remove all "last read" messages in this workflow/user combination
        for message in last_read_message:
            user.last_read.remove(message)
        newest_message = workflow.message_set.last()
        if newest_message is not None:
            user.last_read.add(newest_message)


# Hook into django-registration to make use of our extended form
def user_registered_callback(sender, user, request, **kwargs):
    # hoping that django-registration verifies this form for us.
    user.first_name = request.POST["first_name"]
    user.last_name = request.POST["last_name"]
    profile = CustomerAccount(user=user)
    profile.account_type = request.POST["type"]
    profile.save()

user_registered.connect(user_registered_callback)
