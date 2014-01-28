from django.core.management.base import BaseCommand, CommandError
from digiapproval_project.apps.digiapproval import models
from digiapproval_project.apps.digiapproval.taskforms import *
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
                True, True, workflowspec_three()),
            ("Submit feedback on this service", "This application is for submitting feedback regarding the approval system",
                DIRECTORATES[0], DIRECTORATES_APPROVER_GROUPS[0], DIRECTORATES_DELEGATOR_GROUPS[0],
                True, True, workflowspec_four()),
                ("Apply to hold a public event", 
                "This application will take you through the process of applying for a public events permit,",
                DIRECTORATES[0], DIRECTORATES_APPROVER_GROUPS[0], DIRECTORATES_DELEGATOR_GROUPS[0],
                True, True, workflowspec_realistic_one()),
        ])
        
        self.stdout.write("creating workflows")
        WORKFLOWS = map(to_workflow, [
            (CUSTOMERS[0], WORKFLOW_SPECS[0], APPROVERS[0]),
            (CUSTOMERS[1], WORKFLOW_SPECS[0], APPROVERS[0]),            
            (CUSTOMERS[2], WORKFLOW_SPECS[0], None),
            (ORGANISATIONS[0], WORKFLOW_SPECS[0], APPROVERS[0]),
            (ORGANISATIONS[1], WORKFLOW_SPECS[0], None),
            (CUSTOMERS[0], WORKFLOW_SPECS[1], APPROVERS[1]),
            (CUSTOMERS[1], WORKFLOW_SPECS[1], APPROVERS[1]),            
            (CUSTOMERS[2], WORKFLOW_SPECS[1], None),
            (ORGANISATIONS[0], WORKFLOW_SPECS[1], APPROVERS[1]),
            (ORGANISATIONS[1], WORKFLOW_SPECS[1], None),
            (CUSTOMERS[0], WORKFLOW_SPECS[2], APPROVERS[2]),
            (CUSTOMERS[1], WORKFLOW_SPECS[2], APPROVERS[2]),            
            (CUSTOMERS[2], WORKFLOW_SPECS[2], None),
            (ORGANISATIONS[0], WORKFLOW_SPECS[2], APPROVERS[2]),
            (ORGANISATIONS[1], WORKFLOW_SPECS[2], None),
            (CUSTOMERS[0], WORKFLOW_SPECS[3], APPROVERS[3]),
            (CUSTOMERS[1], WORKFLOW_SPECS[3], APPROVERS[3]),            
            (CUSTOMERS[2], WORKFLOW_SPECS[3], None),
            (ORGANISATIONS[0], WORKFLOW_SPECS[3], APPROVERS[3]),
            (ORGANISATIONS[1], WORKFLOW_SPECS[3], None),
        ])
        
        self.stdout.write("processing workflows")
        PROCESSED_WORKFLOWS = map(process_workflow, [
            (WORKFLOWS[1], 0),
            (WORKFLOWS[2], 1),
            (WORKFLOWS[3], 1),
            (WORKFLOWS[4], 10),
            (WORKFLOWS[6], 0),
            (WORKFLOWS[7], 1),
            (WORKFLOWS[8], 1),
            (WORKFLOWS[9], 10),
            (WORKFLOWS[11], 0),
            (WORKFLOWS[12], 1),
            (WORKFLOWS[13], 1),
            (WORKFLOWS[14], 10),
            (WORKFLOWS[16], 0),
            (WORKFLOWS[17], 1),
            (WORKFLOWS[18], 1),
            (WORKFLOWS[19], 10),
        ])
        

def clear_data():
    """Clears the current data from the database"""
    for user in User.objects.exclude(username='super'):
        user.delete()
    for group in Group.objects.all():
        group.delete()
    for model in [models.Task, models.Workflow, models.WorkflowSpec, models.CustomerAccount, models.UserFile, models.Message]:
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
    
def workflowspec_three():
    
    wf_spec = specs.WorkflowSpec()
    cust_agreement = specs.Simple(wf_spec, "Customer Agreement")
    cust_fieldentry = specs.Simple(wf_spec, "Permit Details")
    approver_agreement = specs.Simple(wf_spec, "Approver Agreement")
    customer_tally = CheckTally.create_exclusive_task(wf_spec, "Choose to read agreement", 20, cust_agreement, cust_fieldentry)

    task_join1 = specs.Join(wf_spec, "Parties In Agreement")
    
    wf_spec.start.connect(approver_agreement)
    wf_spec.start.connect(customer_tally)    
    cust_agreement.connect(cust_fieldentry)
    cust_fieldentry.connect(task_join1)
    approver_agreement.connect(task_join1)
    
    cust_agreement.set_data(task_data = AcceptAgreement.make_task_dict(True, lorum_ipsum, 'CUSTOMER'))
    cust_fieldentry.set_data(task_data = FieldEntry.make_task_dict('CUSTOMER', 
        ('event_name', 'What is the name of your event:  ', 'text', True),
        ('event_purpose', 'What is the purpose of your event: ', 'text', True),
        ('event_love', 'In 50 words or less, why do you love applying for events: ', 'text', True),)
    )
    approver_agreement.set_data(task_data = AcceptAgreement.make_task_dict(True, lorum_ipsum,'APPROVER'))
    customer_tally.set_data(task_data = CheckTally.make_task_dict('CUSTOMER',
        ('like_bureaucracy', "Do you like Bureaucracy: ", False, 5),
        ('like_events', "Do you like throwing events: ", False, 10),
        ('like_digiactive', "Do you like DigiACTive: ", True, 15),)
    )
    
    return wf_spec
    
def workflowspec_four():
    wf_spec = specs.WorkflowSpec()
    cust_agreement = specs.Simple(wf_spec, "Customer Agreement")
    cust_fieldentry = specs.Simple(wf_spec, "Permit Details")
    approver_agreement = specs.Simple(wf_spec, "Approver Agreement")
    task_join1 = specs.Join(wf_spec, "Parties In Agreement")
    cust_upload = specs.Simple(wf_spec, "Upload Cheque")
    approver_choice = ChooseBranch.create_exclusive_task(wf_spec, "Accept Agreement or skip", 
        (1, approver_agreement), 
        (2, task_join1)

    )
    customer_choice = ChooseBranches.create_multichoice_task(wf_spec, "Choose tasks",
        (1, cust_agreement),
        (2, cust_fieldentry),
        (3, cust_upload),
    )
    
    
    wf_spec.start.connect(customer_choice)
    wf_spec.start.connect(approver_choice)
    cust_agreement.connect(task_join1)
    cust_fieldentry.connect(task_join1)
    approver_agreement.connect(task_join1)
    
    cust_agreement.set_data(task_data = AcceptAgreement.make_task_dict(True, lorum_ipsum, 'CUSTOMER'))
    cust_fieldentry.set_data(task_data = FieldEntry.make_task_dict('CUSTOMER', 
        ('event_name', 'What is the name of your event:  ', 'text', True),
        ('event_purpose', 'What is the purpose of your event: ', 'text', True),
        ('event_love', 'In 50 words or less, why do you love applying for events: ', 'text', True),)
    )
    cust_upload.set_data(task_data = FileUpload.make_task_dict(True, 'CUSTOMER'))
    approver_agreement.set_data(task_data = AcceptAgreement.make_task_dict(True, lorum_ipsum,'APPROVER'))
    
    customer_choice.set_data(task_data = ChooseBranches.make_task_dict('CUSTOMER', 1,
        ('agreement', "Read and accept agreement", 1),
        ('field_entry', "Go straight to field entry", 2),
        ('cust_upload', "Upload most recently signed bank checque", 3),)
    )
    
    approver_choice.set_data(task_data = ChooseBranch.make_task_dict('APPROVER', 
        ('agreement', "Read and accept agreement", 1),
        ('skip', "Skip to next action", 2))
    )
    
    return wf_spec
    
def workflowspec_realistic_one():
    """Workflow spec representative of actual TAMS processes
    """
    wf_spec = specs.WorkflowSpec()
    cust_agreement = specs.Simple(wf_spec, "Customer Usage Agreement")
    appr_agreement = specs.Simple(wf_spec, "Approver Usage Agreement")
    
    #Entry taskforms
    cust_event_info = specs.Simple(wf_spec, "Basic Event Description")
    cust_upload_ramp = specs.Simple(wf_spec, "Upload Risk Assessment Management Plan")
    appr_join1 = specs.Join(wf_spec, "Workflow Assessment Join 1")
    appr_join2 = specs.Join(wf_spec, "Workflow Assessment Join 2")
    cust_upload_insure = specs.Simple(wf_spec, "Upload Insurance Policy")
    cust_waste_plan = specs.Simple(wf_spec, "Upload Waste Management Plan")
    cust_traffic_plan = specs.Simple(wf_spec, "Upload Traffic Plan")

    #Branching taskforms
    cust_ramp_tally = CheckTally.create_exclusive_task(wf_spec, "Preliminary Risk Assessment", 40, 
                                                            cust_upload_ramp, appr_join1)
    
    cust_event_attendance = ChooseBranch.create_exclusive_task(wf_spec, "Participant attendance expectation",
        (1, cust_upload_ramp),
        (2, cust_ramp_tally)
    )
                                                            
    cust_insurance_req = ChooseBranch.create_exclusive_task(wf_spec, "Event insurance requirement",
        (1, cust_upload_insure),
        (2, appr_join1)
    )
    
    appr_review1 = ChooseBranches.create_multichoice_task(wf_spec, 'Review and Assign Tasks',
        (1, cust_waste_plan),
        (2, cust_traffic_plan)
    )

    
    #S1: Agreement acceptance
    cust_agreement.set_data(task_data = AcceptAgreement.make_task_dict(True, cust_agreement_text, 'CUSTOMER'))
    appr_agreement.set_data(task_data = AcceptAgreement.make_task_dict(True, appr_agreement_text, 'APPROVER'))
    wf_spec.start.connect(cust_agreement)
    wf_spec.start.connect(appr_agreement)
    
    #S2: Event Info form
    cust_event_info.set_data(task_data = FieldEntry.make_task_dict('CUSTOMER',
        ('event_name', "What is the name of your proposed event: ", 'text', True),
        ('event_description', "Please describe the nature of your event: ", 'text', True),
        ('event_public_land', "Is your event planned on Public Unleased Land?", 'checkbox', False),
        ('info_first_event', "Is this the first time you've organised an event?" , 'checkbox', False),
        ('event_other', "Please enter any relevant comments about your event: ", 'text', False),
        task_info="""Welcome to the <b>DigiApproval</b> system. 
If you have any concern during your application process please contact your assigned assessor."""
    ))
    cust_agreement.connect(cust_event_info)
    cust_event_attendance.set_data(task_data = ChooseBranch.make_task_dict('CUSTOMER',
        ('need_ramp', "Over 50 participants are expected to attend", 1),
        ('assess_ramp', "Less than 50 participants are expected to attend ", 2),
        task_info="""In order to assess your need for a <b>Risk Assessment Management Plan</b> (RAMP) we require some information on the number of expected attendies."""
    ))
    cust_event_info.connect(cust_event_attendance)
    cust_event_info.connect(cust_insurance_req)
    cust_ramp_tally.set_data(task_data = CheckTally.make_task_dict('CUSTOMER',
        ('public_land', "Is the event held on public land: ", False, 41),
        ('large_structures', "Will there be large structures at your event: ", False, 10),
        ('electircal_equipment', "Will there be electrical cabling: ", False, 20),
        ('water_hazards', "Will there be bodies of water at your event", False, 15),
        ('hazardous_materials', "Does your event involve hazardous materials ", False, 41),
        task_info="""In order to assess your need for a <b>Risk Assessment Management Plan</b> (RAMP) we require some information on the nature of your event."""
    ))
    cust_upload_ramp.set_data(task_data = FileUpload.make_task_dict(True, 'CUSTOMER'),
        task_info="""Please upload a completed <b>Risk Assessment Management Plan</b> (RAMP). 
A template can be found on the DigiApproval website (<a href=\"link.to/ramp_template\">link</a>)""")
    
    cust_upload_ramp.connect(appr_join1)
    cust_insurance_req.set_data(task_data = ChooseBranch.make_task_dict('CUSTOMER',
        ('need_insurance', "My event falls under the requirements of public liability insurance", 1),
        ('no_insurance', "My event does not fall under the requirements of <b>Public Liability Insurance</b>",2),
        task_info="""Some events require the holding of Public Liability Insurance. If you are unsure about if it is required for your event, please refer to our help page (<a href=\"link.to/insurance_help\">link</a>)"""
    ))
    cust_upload_insure.set_data(task_data = FileUpload.make_task_dict(True, 'CUSTOMER'),
        task_info="""Please upload proof of your <b>Public Liability Insurance</b> for this event. 
If you need assistance applying for cover, please refer to our help page (<a href=\"link.to/insurance_help\">link</a>)"""
    )
    
    #S3: Approval stage
    appr_review1.set_data(task_data = ChooseBranches.make_task_dict('APPROVER',
        ('waste_plan', "Assign Waste Management Plan", 1),
        ('traffic_plan', "Assign Traffic Management Plan", 2),
        task_info = """Please review the previously completed stages and, if appropriate, assign further tasks for the customer to complete"""
        
    ))
    appr_join1.connect(appr_review1)
    appr_join1.connect(appr_join2)
    
    #S4: Second application stage
    cust_waste_plan.set_data(task_data = FileUpload.make_task_dict(True, 'CUSTOMER'), 
        task_info="""Please upload a completed <b>Waste Management Plan</b>. 
A template can be found on the DigiApproval website (<a href=\"link.to/waste_management_plan_template\">link</a>)"""
    )
    cust_traffic_plan.set_data(task_data = FileUpload.make_task_dict(True, 'CUSTOMER'),
        task_info="""Please upload a completed <b>Traffic Management Plan</b>. 
A template can be found on the DigiApproval website (<a href=\"link.to/traffic_management_plan_template\">link</a>)"""
    )
    cust_waste_plan.connect(appr_join2)
    cust_traffic_plan.connect(appr_join2)
    
    return wf_spec
    
    
    
    
    
    
    
    
#Dummy text for agreements    
lorum_ipsum = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer sollicitudin ultrices elementum. Nam vel luctus tortor. Sed pretium sodales dui. Nullam id ante a metus ultricies sagittis. Vestibulum porttitor pretium imperdiet. Curabitur dolor est, euismod quis tellus a, volutpat scelerisque felis. Sed ac venenatis libero. Fusce quis tortor nec arcu malesuada faucibus sed at tellus. Fusce a consectetur magna. Integer ullamcorper sollicitudin ligula. Donec interdum luctus nisl ac eleifend. Nunc lobortis quam non nisl laoreet, quis fermentum elit sagittis.

Maecenas lobortis pretium volutpat. Phasellus et arcu aliquet purus varius tincidunt. Integer a libero turpis. Nunc iaculis orci et gravida auctor. Etiam feugiat porta orci a auctor. Sed sagittis semper fringilla. In non dapibus augue, id pharetra eros. Suspendisse felis neque, posuere et lobortis eget, tempus vel leo. Proin suscipit justo id eros rhoncus molestie. Sed dignissim sagittis diam eu mattis. Donec vestibulum mauris in massa pulvinar pretium at blandit nunc. Sed placerat eros metus, ac interdum ante sagittis sed. Nulla pretium convallis sapien, nec accumsan urna pharetra ac.

Pellentesque ullamcorper scelerisque justo et sagittis. Sed tempor nisl at purus luctus, a fermentum libero condimentum. Cras eu nibh porta, venenatis ligula eget, auctor lacus. Etiam eu aliquam sapien. Fusce nisi sapien, aliquam elementum odio vel, lacinia facilisis eros. Nam lacinia sed risus bibendum convallis. Curabitur blandit libero et mi aliquet, tincidunt lacinia elit pellentesque. Maecenas ultrices quis lacus ac egestas. Praesent eu elementum arcu.

Vivamus condimentum sapien non ultrices interdum. Nullam dignissim, elit quis consectetur convallis, dui ipsum commodo lorem, sit amet eleifend lectus lacus non eros. Etiam dapibus elit et enim viverra commodo. Pellentesque sit amet imperdiet massa, vitae aliquet augue. Proin lacinia egestas diam eu mattis. Vestibulum pretium lobortis lectus, a scelerisque risus pretium at. Cras malesuada sapien eu mauris suscipit lacinia. Phasellus et accumsan lorem, interdum pretium neque. Curabitur magna nibh, sollicitudin at magna at, rhoncus fringilla quam. Vivamus nec accumsan est. Maecenas hendrerit ut sapien eu auctor.

Morbi imperdiet mauris et mi suscipit tempor. Aenean congue risus ac ante aliquet interdum. Integer metus ligula, luctus vel nisi sed, blandit varius elit. Nam et purus quis tortor faucibus faucibus et quis ipsum. In nibh orci, pretium nec elementum at, malesuada eget ligula. Phasellus imperdiet tempus hendrerit. Sed ut sollicitudin augue, eu molestie mauris. In consequat aliquet dui vitae vulputate. Aliquam vitae dolor a sapien cursus sagittis in vitae magna. Fusce rutrum arcu a eros facilisis sodales. """

cust_agreement_text = """By accepting this agreement you acknowledge your reading and acceptance of both the ACT Government Acceptable Use of ICT Resources Policy and DigiApproval Fair Use agreement. Any information you provide throughout the application process is true and correct to the best of your knowledge. This service provides no warranty with regards to your application process."""

appr_agreement_text = """By accepting this agreement you acknowledge your reading and acceptance of both the ACT Government Acceptable Use of ICT Resources Policy and DigiApproval Fair Use agreement. Any information you provide throughout the application process is true and correct to the best of your knowledge. You agree to assess this application with complete impartiality and in accordance with the relevant legislation and business rules. This service provides no warranty with regards to your application process."""   


