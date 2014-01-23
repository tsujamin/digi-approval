from django.core.management.base import BaseCommand, CommandError
from digiapproval_project.apps.digiapproval import models
from digiapproval_project.apps.digiapproval.taskforms import AcceptAgreement, FieldEntry
from django.contrib.auth.models import User, Group
from SpiffWorkflow import specs

class Command(BaseCommand):
    """ruby rake db:migrate"""
    
    args = '<>'
    help = 'Initialises the database and fills it with the test fixtures'
    
    def handle(self, *args, **kwargs):
        """Clears current models from tables, creates demo directorates, approvers, orginisations and customers"""
        self.stdout.write("Clearing current models")   
        clear_data()
        
        self.stdout.write("Creating directorate groups (django.contrib.auth)")   
        DIRECTORATES = map(directorate_to_group, [ 
            'Territory and Municipal Services Directorate',
            'Justice and Community Safety Directorate',
            'National Capital Authority',
            'Australian Federal Police',
            'Commerce and Works Directorate'
        ])
        
        self.stdout.write("Creating directorate approver groups (django.contrib.auth)")   
        DIRECTORATES_APPROVER_GROUPS = map(directorate_to_group, [
            'TAMS - Parks and City Services - City Services - Licensing and Compliance',
            'JACS - Emergency Services Agency - Emergency Management, Risk & Spatial Services',
            'NCA - National Capital Estate Unit - Estate Management',
            'AFP - ACT Policing - Emergency Management and Planning',
            'CWD - ACT Insurance Authority'
        ])
        
        self.stdout.write("Creating directorate delegator groups (django.contrib.auth)")   
        DIRECTORATES_DELEGATOR_GROUPS = map(directorate_to_group, [g.name[:67] + " (Delegators)" for g in DIRECTORATES_APPROVER_GROUPS])
        
        
        self.stdout.write("creating approver accounts (django.contrib.auth)")   
        APPROVERS = map(approver_to_user, [
            ('David Potter', 'harrysorrydavid', 'David.Potter@act.gov.au', [DIRECTORATES[0], DIRECTORATES_APPROVER_GROUPS[0], DIRECTORATES_DELEGATOR_GROUPS[0]]),
            ('Cal McGregor', 'alwaystheminister', 'Cal.McGregor@act.gov.au', [DIRECTORATES[0], DIRECTORATES_APPROVER_GROUPS[0]]),
            ('Claudia Marshall', 'neverthetwotermer', 'Claudia.Marshall@nationalcapital.gov.au', [DIRECTORATES[2], DIRECTORATES_APPROVER_GROUPS[2], DIRECTORATES_DELEGATOR_GROUPS[2]]),
            ('Joe Sandilands', 'attorneygeneral', 'Joe.Sandilands@afp.gov.au', [DIRECTORATES[3], DIRECTORATES_APPROVER_GROUPS[3], DIRECTORATES_DELEGATOR_GROUPS[3]]),
            ('Lincoln Lincoln', 'lincolnlincoln', 'Lincoln.Lincoln@act.gov.au', [DIRECTORATES[4], DIRECTORATES_APPROVER_GROUPS[4]]),
        ])
        
        self.stdout.write("creating organisation accounts (CustomerAccount)")
        ORGANISATIONS= map(to_customer_account, [
            ('ORGANISATION', 'leaky_plumbing', 'wikiwho?', 'webmaster@leakyplumbing.org.au', []),
            ('ORGANISATION', 'kirstys_short_term_loans', 'kneecaps', 'col@kirstys.net.au', []),
        ])
        
        self.stdout.write("creating customer accounts (CustomerAccount)")
        CUSTOMERS = map(to_customer_account, [
            ('CUSTOMER', 'cleaver_g', 'fubar', 'clever_cleaver167@yahoo.com', []),
            ('CUSTOMER', 'missy_tanner', 'harrysorryjoshua', 'missy@hotmail.com', [ORGANISATIONS[0]]),
            ('CUSTOMER', 'j_floyd', 'ihaveaguy', 'joshua.floyd@leakyplumbing.org.au', [ORGANISATIONS[0]]),
            ('CUSTOMER', 'la_hole', '5stars', 'lane_hold@laneholdings.com.au', []),
        ])
        
        self.stdout.write("creating workflow specifications")
        WORKFLOW_SPECS = map(to_workflow_spec, [
            ("Veterinary Visit Permit", "This application is for a Veterinary Visit Permit pursuant to the <i>Animal Welfare Act 1992</i>. Applicants must demonstrate that they don't hate animals.",
                DIRECTORATES[0], DIRECTORATES_APPROVER_GROUPS[0], DIRECTORATES_DELEGATOR_GROUPS[0],
                True, True, workflowspec_one()),
            ("Police Checkup Request", "This application is for a National Police Certificate from the Australian Federal Police. A National Police Certificate will list all unspent convictions in the applicant's criminal history.",
                DIRECTORATES[3], DIRECTORATES_APPROVER_GROUPS[3], DIRECTORATES_DELEGATOR_GROUPS[3],
                True, True, workflowspec_two()),
            ("Request to Ban Persons from Private Businesses", "This application is for a permit to ban persons from entering designated private premises during a declared State of Emergency.",
                DIRECTORATES[2], DIRECTORATES_APPROVER_GROUPS[2], DIRECTORATES_DELEGATOR_GROUPS[2],
                False, True, workflowspec_two())
        ])
        
        self.stdout.write("creating workflows")
        WORKFLOWS = map(to_workflow, [
            (CUSTOMERS[0], WORKFLOW_SPECS[0], APPROVERS[0]),
            (CUSTOMERS[1], WORKFLOW_SPECS[2], APPROVERS[2]),            
            (CUSTOMERS[2], WORKFLOW_SPECS[0], None),
            (ORGANISATIONS[0], WORKFLOW_SPECS[0], APPROVERS[1]),
            (ORGANISATIONS[1], WORKFLOW_SPECS[0], None),
            (CUSTOMERS[0], WORKFLOW_SPECS[1], APPROVERS[3]),
            (CUSTOMERS[1], WORKFLOW_SPECS[1], APPROVERS[3]),            
            (CUSTOMERS[2], WORKFLOW_SPECS[1], None),
            (ORGANISATIONS[0], WORKFLOW_SPECS[1], APPROVERS[3]),
            (ORGANISATIONS[1], WORKFLOW_SPECS[1], None),
        ])
        
        self.stdout.write("processing workflows")
        PROCESSED_WORKFLOWS = map(process_workflow, [
            (WORKFLOWS[1], 0),
            (WORKFLOWS[2], 1),
            (WORKFLOWS[3], 1),
            (WORKFLOWS[4], 10),
            (WORKFLOWS[5], 0),
            (WORKFLOWS[6], 1),
            (WORKFLOWS[7], 1),
            (WORKFLOWS[8], 10),
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
    user = User.objects.create_user(email[:email.find('@')], email, password)
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
    
def to_workflow_spec((name, description, owner, delegators, approvers, public, toplevel, wf_spec)):
    """Returns a WorkflowSpec model from parameter tuple"""
    spec_model = models.WorkflowSpec(name=name, description=description, \
        owner=owner, delegators=delegators, approvers=approvers, \
            public=public, toplevel=toplevel, spec=wf_spec)
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
    
def workflowspec_two():
    wf_spec = specs.WorkflowSpec()
    cust_agreement = specs.Simple(wf_spec, "Customer Agreement")
    cust_fieldentry = specs.Simple(wf_spec, "Permit Details")
    approver_agreement = specs.Simple(wf_spec, "Approver Agreement")
    task_join1 = specs.Join(wf_spec, "Parties In Agreement")
    
    wf_spec.start.connect(cust_fieldentry)
    wf_spec.start.connect(approver_agreement)
    cust_fieldentry.connect(cust_agreement)
    cust_agreement.connect(task_join1)
    approver_agreement.connect(task_join1)
    
    cust_agreement.set_data(task_data = AcceptAgreement.make_task_dict(True, lorum_ipsum, 'CUSTOMER'))
    cust_fieldentry.set_data(task_data = FieldEntry.make_task_dict('CUSTOMER', 
        ('event_name', 'What is the name of your event:  ', 'text', True),
        ('event_purpose', 'What is the purpose of your event: ', 'text', True),
        ('event_love', 'In 50 words or less, why do you love applying for events: ', 'text', True),)
    )
    approver_agreement.set_data(task_data = AcceptAgreement.make_task_dict(True, lorum_ipsum,'APPROVER'))
    return wf_spec
    
    
#Dummy text for agreements    
lorum_ipsum = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer sollicitudin ultrices elementum. Nam vel luctus tortor. Sed pretium sodales dui. Nullam id ante a metus ultricies sagittis. Vestibulum porttitor pretium imperdiet. Curabitur dolor est, euismod quis tellus a, volutpat scelerisque felis. Sed ac venenatis libero. Fusce quis tortor nec arcu malesuada faucibus sed at tellus. Fusce a consectetur magna. Integer ullamcorper sollicitudin ligula. Donec interdum luctus nisl ac eleifend. Nunc lobortis quam non nisl laoreet, quis fermentum elit sagittis.

Maecenas lobortis pretium volutpat. Phasellus et arcu aliquet purus varius tincidunt. Integer a libero turpis. Nunc iaculis orci et gravida auctor. Etiam feugiat porta orci a auctor. Sed sagittis semper fringilla. In non dapibus augue, id pharetra eros. Suspendisse felis neque, posuere et lobortis eget, tempus vel leo. Proin suscipit justo id eros rhoncus molestie. Sed dignissim sagittis diam eu mattis. Donec vestibulum mauris in massa pulvinar pretium at blandit nunc. Sed placerat eros metus, ac interdum ante sagittis sed. Nulla pretium convallis sapien, nec accumsan urna pharetra ac.

Pellentesque ullamcorper scelerisque justo et sagittis. Sed tempor nisl at purus luctus, a fermentum libero condimentum. Cras eu nibh porta, venenatis ligula eget, auctor lacus. Etiam eu aliquam sapien. Fusce nisi sapien, aliquam elementum odio vel, lacinia facilisis eros. Nam lacinia sed risus bibendum convallis. Curabitur blandit libero et mi aliquet, tincidunt lacinia elit pellentesque. Maecenas ultrices quis lacus ac egestas. Praesent eu elementum arcu.

Vivamus condimentum sapien non ultrices interdum. Nullam dignissim, elit quis consectetur convallis, dui ipsum commodo lorem, sit amet eleifend lectus lacus non eros. Etiam dapibus elit et enim viverra commodo. Pellentesque sit amet imperdiet massa, vitae aliquet augue. Proin lacinia egestas diam eu mattis. Vestibulum pretium lobortis lectus, a scelerisque risus pretium at. Cras malesuada sapien eu mauris suscipit lacinia. Phasellus et accumsan lorem, interdum pretium neque. Curabitur magna nibh, sollicitudin at magna at, rhoncus fringilla quam. Vivamus nec accumsan est. Maecenas hendrerit ut sapien eu auctor.

Morbi imperdiet mauris et mi suscipit tempor. Aenean congue risus ac ante aliquet interdum. Integer metus ligula, luctus vel nisi sed, blandit varius elit. Nam et purus quis tortor faucibus faucibus et quis ipsum. In nibh orci, pretium nec elementum at, malesuada eget ligula. Phasellus imperdiet tempus hendrerit. Sed ut sollicitudin augue, eu molestie mauris. In consequat aliquet dui vitae vulputate. Aliquam vitae dolor a sapien cursus sagittis in vitae magna. Fusce rutrum arcu a eros facilisis sodales. """  


