from django.core.management.base import BaseCommand, CommandError
from digiapproval_project.apps.digiapproval import models
from digiapproval_project.apps.digiapproval.taskforms import AcceptAgreement
from django.contrib.auth.models import User, Group
from SpiffWorkflow import specs

class Command(BaseCommand):
    """ruby rake db:migrate"""
    
    args = '<>'
    help = 'Initialises the database and fills it with the test fixtures'
    
    def handle(self, *args, **kargs):
        """Clears current models from tables, creates demo directorates, approvers, orginisations and customers"""
        self.stdout.write("clearing current models")   
        clear_data()
        
        self.stdout.write("creating directorate groups(django.contrub.auth)")   
        DIRECTORATES = map(directorate_to_group, [ 
            'TAMS', 
            'NCA',
        ])
        
        self.stdout.write("creating approver accounts(django.contrub.auth)")   
        APPROVERS = map(approver_to_user, [
            ('David Potter', 'harrysorrydavid', 'David.Potter@act.gov.au', [DIRECTORATES[0]]),
            ('Cal McGregor', 'alwaystheminister', 'Cal.McGregor@act.gov.au', [DIRECTORATES[0]]),
            ('Claudia Marshall', 'neverthetwotermer', 'Claudia.Marshall@nca.gov.au', [DIRECTORATES[0], DIRECTORATES[1]]),
        ])
        
        self.stdout.write("creating organisation accounts(CustomerAccount)")
        ORGANISATIONS= map(to_customer_account, [
            ('ORGANISATION', 'leaky_plumbing', 'wikiwho?', 'webmaster@leakyplumbing.org.au', []),
            ('ORGANISATION', 'kirstys_short_term_loans', 'kneecaps', 'col@kirstys.net.au', []),
        ])
        
        self.stdout.write("creating customer accounts(CustomerAccount)")
        CUSTOMERS = map(to_customer_account, [
            ('CUSTOMER', 'cleaver_g', 'fubar', 'clever_cleaver167@yahoo.com', []),
            ('CUSTOMER', 'missy_tanner', 'harrysorryjoshua', 'missy@hotmail.com', [ORGANISATIONS[0]]),
            ('CUSTOMER', 'j_floyd', 'ihaveaguy', 'joshua.floyd@leakyplumbing.org.au', [ORGANISATIONS[0]]),
            ('CUSTOMER', 'la_hole', '5stars', 'lane_hold@laneholdings.com.au', []),
        ])
        
        self.stdout.write("creating workflow specifications")
        WORKFLOW_SPECS = map(to_workflow_spec, [
            ("Veterinary Visit Permit", DIRECTORATES[0], True, workflowspec_one()),
            ("Police Checkup Request", DIRECTORATES[1], False, workflowspec_one()),
        ])
        
        self.stdout.write("creating workflows")
        WORKFLOWS = map(to_workflow, [
            (CUSTOMERS[0], WORKFLOW_SPECS[0], APPROVERS[0]),
            (CUSTOMERS[1], WORKFLOW_SPECS[0], APPROVERS[2]),            
            (CUSTOMERS[2], WORKFLOW_SPECS[0], None),
            (ORGANISATIONS[0], WORKFLOW_SPECS[0], APPROVERS[1]),
            (ORGANISATIONS[1], WORKFLOW_SPECS[0], None),
        ])
        
        self.stdout.write("processing workflows")
        PROCESSED_WORKFLOWS = map(process_workflow, [
            (WORKFLOWS[1], 0),
            (WORKFLOWS[2], 1),
            (WORKFLOWS[3], 1),
            (WORKFLOWS[4], 10),
        ])
        

def clear_data():
    """Clears the current data from the database"""
    for user in User.objects.exclude(username='super'):
        user.delete()
    for group in Group.objects.all():
        group.delete()
    for model in [models.Task, models.Workflow, models.WorkflowSpec, models.CustomerAccount, models.UserFile]:
        for instance in model.objects.all():
            instance.delete()

#Tuple map functions
def directorate_to_group(group_name):
    """Returns django.contrib.auth group created from parameter name"""
    group = Group(name=group_name)
    group.save()
    return group
    
def approver_to_user((name, password, email, groups)):
    """Returns django.contrib.auth user created from parameter tuple"""
    user = User.objects.create_user(email, email, password)
    user.first_name, user.last_name = name.split()
    user.save()
    for group in groups:
        user.groups.add(group)
    return user
    
def to_customer_account((account_type, username, password, email, parents)):
    """Returns customer account created from parameter tuple"""
    user = User.objects.create_user(username, email, password)
    user.save()
    customer = models.CustomerAccount(account_type = account_type, user = user)
    customer.save()
    for parent in parents:
        customer.parent_accounts.add(parent)
    return customer
    
def to_workflow_spec((name, group, public, wf_spec)):
    """Returns a WorkflowSpec model from parameter tuple"""
    spec_model = models.WorkflowSpec(name = name, owner = group, public = public, spec = wf_spec)
    spec_model.save()
    return spec_model
    
def to_workflow((customer, spec, approver)):
    workflow = spec.start_workflow(customer)
    if approver is not None:
        workflow.approver = approver
    workflow.save()
    return workflow
    
def process_workflow((workflow, complete_tasks)):
    counter = 0
    while counter is not complete_tasks:
        workflow.get_ready_task_forms()
        workflow.workflow.complete_next()
        counter += 1
        if workflow.workflow.is_completed():
            break
    workflow.save()
    return workflow
    
    
    
def workflowspec_one():
    wf_spec = specs.WorkflowSpec()
    cust_agreement = specs.Simple(wf_spec, "Customer Agreement")
    approver_agreement = specs.Simple(wf_spec, "Approver Agreement")
    agreement_join = specs.Join(wf_spec, "Parties In Agreement")
    
    wf_spec.start.connect(cust_agreement)
    wf_spec.start.connect(approver_agreement)
    cust_agreement.connect(agreement_join)
    approver_agreement.connect(agreement_join)
    
    cust_agreement.set_data(task_data = AcceptAgreement.make_task_dict(True, lorum_ipsum, 'CUSTOMER'))
    approver_agreement.set_data(task_data = AcceptAgreement.make_task_dict(True, lorum_ipsum, 'APPROVER') )
    return wf_spec
    
    
#Dummy text for agreements    
lorum_ipsum = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer sollicitudin ultrices elementum. Nam vel luctus tortor. Sed pretium sodales dui. Nullam id ante a metus ultricies sagittis. Vestibulum porttitor pretium imperdiet. Curabitur dolor est, euismod quis tellus a, volutpat scelerisque felis. Sed ac venenatis libero. Fusce quis tortor nec arcu malesuada faucibus sed at tellus. Fusce a consectetur magna. Integer ullamcorper sollicitudin ligula. Donec interdum luctus nisl ac eleifend. Nunc lobortis quam non nisl laoreet, quis fermentum elit sagittis.

Maecenas lobortis pretium volutpat. Phasellus et arcu aliquet purus varius tincidunt. Integer a libero turpis. Nunc iaculis orci et gravida auctor. Etiam feugiat porta orci a auctor. Sed sagittis semper fringilla. In non dapibus augue, id pharetra eros. Suspendisse felis neque, posuere et lobortis eget, tempus vel leo. Proin suscipit justo id eros rhoncus molestie. Sed dignissim sagittis diam eu mattis. Donec vestibulum mauris in massa pulvinar pretium at blandit nunc. Sed placerat eros metus, ac interdum ante sagittis sed. Nulla pretium convallis sapien, nec accumsan urna pharetra ac.

Pellentesque ullamcorper scelerisque justo et sagittis. Sed tempor nisl at purus luctus, a fermentum libero condimentum. Cras eu nibh porta, venenatis ligula eget, auctor lacus. Etiam eu aliquam sapien. Fusce nisi sapien, aliquam elementum odio vel, lacinia facilisis eros. Nam lacinia sed risus bibendum convallis. Curabitur blandit libero et mi aliquet, tincidunt lacinia elit pellentesque. Maecenas ultrices quis lacus ac egestas. Praesent eu elementum arcu.

Vivamus condimentum sapien non ultrices interdum. Nullam dignissim, elit quis consectetur convallis, dui ipsum commodo lorem, sit amet eleifend lectus lacus non eros. Etiam dapibus elit et enim viverra commodo. Pellentesque sit amet imperdiet massa, vitae aliquet augue. Proin lacinia egestas diam eu mattis. Vestibulum pretium lobortis lectus, a scelerisque risus pretium at. Cras malesuada sapien eu mauris suscipit lacinia. Phasellus et accumsan lorem, interdum pretium neque. Curabitur magna nibh, sollicitudin at magna at, rhoncus fringilla quam. Vivamus nec accumsan est. Maecenas hendrerit ut sapien eu auctor.

Morbi imperdiet mauris et mi suscipit tempor. Aenean congue risus ac ante aliquet interdum. Integer metus ligula, luctus vel nisi sed, blandit varius elit. Nam et purus quis tortor faucibus faucibus et quis ipsum. In nibh orci, pretium nec elementum at, malesuada eget ligula. Phasellus imperdiet tempus hendrerit. Sed ut sollicitudin augue, eu molestie mauris. In consequat aliquet dui vitae vulputate. Aliquam vitae dolor a sapien cursus sagittis in vitae magna. Fusce rutrum arcu a eros facilisis sodales. """  


