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
        ('ORGANISATION', 'Organisation account'),
    )
    
    user = models.OneToOneField(User) 
    account_type = models.CharField(max_length=16,
                                    choices=ACCOUNT_TYPE_CHOICES, 
                                    default='CUSTOMER')
    parent_accounts = models.ManyToManyField(  'self',
                                                symmetrical=False,
                                                related_name='sub_accounts',
                                                blank = True, null = True)
        
    def get_own_workflows(self, *args, **kwargs): #UNTESTED
        """Get workflows owned by this user, takes **kwarg of ['completed'] as filter, otherwise returns all"""
        if 'completed' in kwargs:
            return workflow_customer.get(completed=bool(kwargs['completed']))
        else:
            return workflow_customer.all()
    
    def get_all_workflows(self, *args, **kwargs): #UNTESTED
        """Gets workflows of self and parent accounts, takes **kwarg of ['completed'] as filter, otherwise returns all"""
        workflow_list = self.get_own_workflows(*args, **kwargs)
        for parent in self.parent_accounts:
            workflow_list.extend(parent.get_own_workflows(*args, **kwargs))
        return workflow_list
            
        
    def save(self, *args, **kwargs): ##DOESNT VALIDATE PROPERLY ON THE FIRST DJANGO-ADMIN SAVE, DOES AFTER THAT. MANY TO MANY NOT SAVING?
        """Saves related auth.User object. Checks types of related accounts for legality (ie customer doesnt have sub accounts)"""
        from exceptions import ValueError
        if self.id: #already saved
            if self.account_type == 'CUSTOMER':
                if self.sub_accounts.count() != 0:
                    raise ValueError("Customers cannot have sub accounts")
                if self.parent_accounts.filter(account_type='CUSTOMER').count() != 0:
                    raise ValueError("Parent Accounts must be Organisations")
            elif self.account_type  == 'ORGANISATION':
                if self.parent_accounts.count() != 0:
                    raise ValueError("Organisations cannot have parent accounts")
                if self.sub_accounts.filter(account_type='ORGANISATION').count() != 0:
                    raise ValueError("Sub accounts must be customers")
        try: #Save related user, exceptions will be emitted in CustomerAccount.save()
            self.user.save()
        finally:
            super(CustomerAccount, self).save(*args, **kwargs)
            
    def __unicode__(self):
        return self.account_type + ": " + self.user.username
        
                


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
    
 
    def save(self, *args, **kwargs):
        """Auto assigns approver if none provided"""
        
        from django.core.exceptions import ObjectDoesNotExist
        try:
            self.approver
        except ObjectDoesNotExist:
            self.assign_approver()
        super(Workflow, self).save(*args, **kwargs)    