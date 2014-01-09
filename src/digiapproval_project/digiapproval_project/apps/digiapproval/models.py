from __future__ import absolute_import
from django.db import models
from .fields import WorkflowField, WorkflowSpecField
from django.contrib.auth.models import User, Group

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
    """ End user model. Can either be Customer (single user) or Organisation (User with sub accounts)
        Related accounts of Organisation must be a list of users. Organisations can add users to this list
        Related accounts of User are the organisations it is a part of and whose workflows it can use."""
    
    ACCOUNT_TYPE_CHOICES = (
        ('CUSTOMER', 'Customer account'),
        ('ORGANISATION', 'Organisation account (Customer)'),
    )
    
    user = models.OneToOneField(User) 
    account_type = models.CharField(max_length=16,
                                    choices=ACCOUNT_TYPE_CHOICES, 
                                    default='CUSTOMER')
    related_accounts = models.ManyToManyField(  'self',
                                                symmetrical = False)
    
    def get_member_organisations(self, *args, **kargs):
        """Gets a the organisations a customer is a member of. Throws if self isnt a customer."""
        
    def get_organisation_members(self, *args, **kargs):
        """Gets the members of an organistaion, Throws if self isnt an organisation"""
        
    def get_workflows(self, *args, **kargs):
        """Get workflows owned by this user, takes **karg of ['completed'] as filter"""
        
    def save(self, *args, **kargs):
        """Saves related auth.User object. Checks types of related accounts for legality"""


class WorkflowSpec(models.Model):  
      
    name = models.CharField(max_length = "64")
    owner = models.ForeignKey(Group)
    public = models.BooleanField(default=False)
    spec = WorkflowSpecField()
    
class Workflow(models.Model):
    
    customer = models.ForeignKey(CustomerAccount, related_name='workflow_customer')
    approver = models.ForeignKey(User, related_name='workflow_approver')
    workflow = WorkflowField()
    completed = models.BooleanField(default=False)
    spec = models.ForeignKey(WorkflowSpec)
    

    def assign_approver(self):
        """Finds the least busy approver (in the owner group of the Workflows spec), 
        returns and assigns it to the workflow"""
        
        from django.contrib.auth.models import User
        if self.spec is None:
            raise UnboundLocalError("Workflow has no assigned WorkflowSpec")
        active_approvers = User.objects.filter(groups=self.spec.owner, 
                                                is_active=True)
        #Generates a dict of {Approver: no. current workflows}                                        
        approver_wf_count = dict(map(   lambda x: (x['approver'], x['approver__count']),
                                        Workflow.objects.filter(completed=False, spec__owner=self.spec.owner)
                                            .values('approver')
                                            .annotate(models.Count('approver'))))
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
    
 
    def save(self, *args, **kargs):
        """Auto assigns approver if none provided"""
        
        from django.core.exceptions import ObjectDoesNotExist
        try:
            self.approver
        except ObjectDoesNotExist:
            self.assign_approver()
        super(Workflow, self).save(*args, **kargs)    