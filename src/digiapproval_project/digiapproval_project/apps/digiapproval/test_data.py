# It doesn't make sense to Flake8 this file: it's loads demo data
# flake8: noqa

from functools import partial

from django.contrib.auth.models import User, Group
from SpiffWorkflow import specs

from digiapproval_project.apps.digiapproval import models
from digiapproval_project.apps.digiapproval.taskforms import *


class TestData:
    def __init__(self, _print=lambda msg: None):
        self._print = _print
    
    def create_groups(self):
        self._print("Creating directorate groups (django.contrib.auth)")   
        self.DIRECTORATES = map(directorate_to_group, [ 
            'Territory and Municipal Services Directorate',
            'Justice and Community Safety Directorate',
            'National Capital Authority',
            'Australian Federal Police',
            'Commerce and Works Directorate'
        ])
        
        self._print("Creating directorate approver groups (django.contrib.auth)")   
        self.DIRECTORATES_APPROVER_GROUPS = map(directorate_to_group, [
            'TAMS - Parks and City Services - City Services - Licensing and Compliance',
            'JACS - Emergency Services Agency - Emergency Management, Risk & Spatial Services',
            'NCA - National Capital Estate Unit - Estate Management',
            'AFP - ACT Policing - Emergency Management and Planning',
            'CWD - ACT Insurance Authority'
        ])
        
        self._print("Creating directorate delegator groups (django.contrib.auth)")   
        self.DIRECTORATES_DELEGATOR_GROUPS = map(
            directorate_to_group, 
            [g.name[:67] + " (Delegators)" for g in self.DIRECTORATES_APPROVER_GROUPS])
        
    def create_approvers(self):
        self._print("creating approver accounts (django.contrib.auth)")   
        self.APPROVERS = map(approver_to_user, [
            ('David Potter', 'harrysorrydavid', 'David.Potter@act.gov.au',
             [self.DIRECTORATES[0], self.DIRECTORATES_APPROVER_GROUPS[0],
              self.DIRECTORATES_DELEGATOR_GROUPS[0]]),
            ('Cal McGregor', 'alwaystheminister', 'Cal.McGregor@act.gov.au',
             [self.DIRECTORATES[0], self.DIRECTORATES_APPROVER_GROUPS[0]]),
            ('Claudia Marshall', 'neverthetwotermer',
             'Claudia.Marshall@nationalcapital.gov.au',
             [self.DIRECTORATES[2], self.DIRECTORATES_APPROVER_GROUPS[2],
              self.DIRECTORATES_DELEGATOR_GROUPS[2]]),
            ('Joe Sandilands', 'attorneygeneral', 'Joe.Sandilands@afp.gov.au',
             [self.DIRECTORATES[3], self.DIRECTORATES_APPROVER_GROUPS[3], 
              self.DIRECTORATES_DELEGATOR_GROUPS[3]]),
            ('Lincoln Lincoln', 'lincolnlincoln', 'Lincoln.Lincoln@act.gov.au',
             [self.DIRECTORATES[4], self.DIRECTORATES_APPROVER_GROUPS[4]]),
        ])

    def create_organisations(self):
        self._print("creating organisation accounts (CustomerAccount)")
        self.ORGANISATIONS = map(to_customer_account, [
            ('ORGANISATION', 'Leaky', 'Plumbing', 'leaky_plumbing', 'wikiwho?', 'webmaster@leakyplumbing.org.au', []),
            ('ORGANISATION', 'Kirsty\'s Short', 'Term Loans', 'kirstys_short_term_loans', 'kneecaps', 'col@kirstys.net.au', []),
        ])

    def create_customers(self):
        self._print("creating customer accounts (CustomerAccount)")
        self.CUSTOMERS = map(to_customer_account, [
            ('CUSTOMER', 'Cleaver', 'Greene', 'cleaver_g', 'fubar',
             'clever_cleaver167@yahoo.com', []),
            ('CUSTOMER', 'Melissa', 'Partridge', 'missy_tanner',
              'harrysorryjoshua', 'missy@hotmail.com', [self.ORGANISATIONS[0]]),
            ('CUSTOMER', 'Joshua', 'Floyd', 'j_floyd', 'ihaveaguy',
             'joshua.floyd@leakyplumbing.org.au', [self.ORGANISATIONS[0]]),
            ('CUSTOMER', 'Lane', 'Hold', 'la_hole', '5stars',
             'lane_hold@laneholdings.com.au', []),
            ])

    def create_workflow_specs(self):
        self._print("creating workflow specifications")
        self.WORKFLOW_SPECS = map(to_workflow_spec, [
            ("Veterinary Visit Permit", "This application is for a Veterinary Visit Permit pursuant to the <i>Animal Welfare Act 1992</i>. Applicants must demonstrate that they don't hate animals.",
             self.DIRECTORATES[0], self.DIRECTORATES_APPROVER_GROUPS[0], self.DIRECTORATES_DELEGATOR_GROUPS[0],
             True, True, workflowspec_one()),
            ("Police Checkup Request", "This application is for a National Police Certificate from the Australian Federal Police. A National Police Certificate will list all unspent convictions in the applicant's criminal history.",
             self.DIRECTORATES[3], self.DIRECTORATES_APPROVER_GROUPS[3], self.DIRECTORATES_DELEGATOR_GROUPS[3],
             True, True, workflowspec_two()),
            ("Request to Ban Persons from Private Businesses", "This application is for a permit to ban persons from entering designated private premises during a declared State of Emergency.",
             self.DIRECTORATES[2], self.DIRECTORATES_APPROVER_GROUPS[2], self.DIRECTORATES_DELEGATOR_GROUPS[2],
             True, True, workflowspec_three()),
            ("Submit feedback on this service", "This application is for submitting feedback regarding the approval system",
             self.DIRECTORATES[0], self.DIRECTORATES_APPROVER_GROUPS[0], self.DIRECTORATES_DELEGATOR_GROUPS[0],
             True, True, workflowspec_four()),
            ("Apply to hold a public event", 
             "This application will take you through the process of applying for a public events permit",
             self.DIRECTORATES[0], self.DIRECTORATES_APPROVER_GROUPS[0], self.DIRECTORATES_DELEGATOR_GROUPS[0],
             True, True, workflowspec_realistic_one()),
        ])
        resolve_backpatches(self.WORKFLOW_SPECS)

    def create_workflows(self):
        self._print("creating workflows")
        self.WORKFLOWS = map(to_workflow, [
            (self.CUSTOMERS[0], self.WORKFLOW_SPECS[0], self.APPROVERS[0]),
            (self.CUSTOMERS[1], self.WORKFLOW_SPECS[0], self.APPROVERS[0]),            
            (self.CUSTOMERS[2], self.WORKFLOW_SPECS[0], None),
            (self.ORGANISATIONS[0], self.WORKFLOW_SPECS[0], self.APPROVERS[0]),
            (self.ORGANISATIONS[1], self.WORKFLOW_SPECS[0], None),
            (self.CUSTOMERS[0], self.WORKFLOW_SPECS[1], self.APPROVERS[1]),
            (self.CUSTOMERS[1], self.WORKFLOW_SPECS[1], self.APPROVERS[1]),            
            (self.CUSTOMERS[2], self.WORKFLOW_SPECS[1], None),
            (self.ORGANISATIONS[0], self.WORKFLOW_SPECS[1], self.APPROVERS[1]),
            (self.ORGANISATIONS[1], self.WORKFLOW_SPECS[1], None),
            (self.CUSTOMERS[0], self.WORKFLOW_SPECS[2], self.APPROVERS[2]),
            (self.CUSTOMERS[1], self.WORKFLOW_SPECS[2], self.APPROVERS[2]),            
            (self.CUSTOMERS[2], self.WORKFLOW_SPECS[2], None),
            (self.ORGANISATIONS[0], self.WORKFLOW_SPECS[2], self.APPROVERS[2]),
            (self.ORGANISATIONS[1], self.WORKFLOW_SPECS[2], None),
            (self.CUSTOMERS[0], self.WORKFLOW_SPECS[3], self.APPROVERS[3]),
            (self.CUSTOMERS[1], self.WORKFLOW_SPECS[3], self.APPROVERS[3]),            
            (self.CUSTOMERS[2], self.WORKFLOW_SPECS[3], None),
            (self.ORGANISATIONS[0], self.WORKFLOW_SPECS[3], self.APPROVERS[3]),
            (self.ORGANISATIONS[1], self.WORKFLOW_SPECS[3], None),
        ])
    
        self._print("processing workflows")
        self.PROCESSED_WORKFLOWS = map(process_workflow, [
            (self.WORKFLOWS[1], 0),
            (self.WORKFLOWS[2], 1),
            (self.WORKFLOWS[3], 1),
            (self.WORKFLOWS[4], 10),
            (self.WORKFLOWS[6], 0),
            (self.WORKFLOWS[7], 1),
            (self.WORKFLOWS[8], 1),
            (self.WORKFLOWS[9], 10),
            (self.WORKFLOWS[11], 0),
            (self.WORKFLOWS[12], 1),
            (self.WORKFLOWS[13], 1),
            (self.WORKFLOWS[14], 10),
            (self.WORKFLOWS[16], 0),
            (self.WORKFLOWS[17], 1),
            (self.WORKFLOWS[18], 1),
            (self.WORKFLOWS[19], 10),
        ])

    def clear_data(self):
        """Clears the current data from the database"""
        self._print("Clearing current models")
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
    
def to_customer_account((account_type, first_name, last_name, username, password, email, parents)):
    """Returns customer account created from parameter tuple"""
    user = User.objects.create_user(username, email, password)
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    customer = models.CustomerAccount(account_type = account_type, user = user)
    customer.save()
    for parent in parents:
        customer.parent_accounts.add(parent)
    return customer
    
def to_workflow_spec((name, description, owner, approvers, delegators, public, toplevel, wf_spec_with_id)):
    """Returns a WorkflowSpec model from parameter tuple"""
    spec_model = models.WorkflowSpec(name=name, description=description, \
        owner=owner, delegators=delegators, approvers=approvers, \
            public=public, toplevel=toplevel, spec=wf_spec_with_id[1])
    spec_model.save()
    return (wf_spec_with_id[0], spec_model)
    
def to_workflow((customer, spec, approver)):
    workflow = spec[1].start_workflow(customer)
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

backpatches = []

def backpatch(wfs_internal_id, f, param, f2, backpatched_wfs_internal_id):
    backpatches.append((wfs_internal_id, f, param, f2, backpatched_wfs_internal_id))

def resolve_backpatches(workflowspec_models):
    for backpatch in backpatches:
        # get workflowspec
        source, target = None, None
        for workflowspec_model in workflowspec_models:
            if workflowspec_model[0] == backpatch[0]:
                source = workflowspec_model
            if workflowspec_model[0] == backpatch[4]:
                target = workflowspec_model
        if source == None or target == None:
            raise Exception
        kwargs = {backpatch[2]: backpatch[3](target[1].id)}
        backpatch[1](**kwargs)
        source[1].save()
    
def workflowspec_one():
    wf_spec = specs.WorkflowSpec()
    cust_agreement = specs.Simple(wf_spec, "Customer Agreement")
    approver_agreement = specs.Simple(wf_spec, "Approver Agreement")
    agreement_join = specs.Join(wf_spec, "Parties In Agreement")
    
    # TEST OF SUBWORKFLOW
    subworkflow = specs.Simple(wf_spec, "Realistic Subworkflow")
    backpatch(1, subworkflow.set_data, 'task_data', partial(Subworkflow.make_task_dict, 'CUSTOMER'), 5)
    
    wf_spec.start.connect(cust_agreement)
    wf_spec.start.connect(approver_agreement)
    wf_spec.start.connect(subworkflow)
    cust_agreement.connect(agreement_join)
    approver_agreement.connect(agreement_join)
    
    cust_agreement.set_data(task_data = AcceptAgreement.make_task_dict(True, lorum_ipsum, 'CUSTOMER'))
    approver_agreement.set_data(task_data = AcceptAgreement.make_task_dict(True, lorum_ipsum, 'APPROVER') )
    return (1, wf_spec)
    
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
    return (2, wf_spec)
    
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
        ('like_bureaucracy', "Do you like Bureaucracy", False, 5),
        ('like_events', "Do you like throwing events", False, 10),
        ('like_digiactive', "Do you like DigiACTive", True, 15),)
    )
    
    return (3, wf_spec)
    
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
        (cust_agreement.name, "Read and accept agreement", 1),
        (cust_fieldentry.name, "Go straight to field entry", 2),
        (cust_upload.name, "Upload most recently signed bank checque", 3),)
    )
    
    approver_choice.set_data(task_data = ChooseBranch.make_task_dict('APPROVER', 
        (approver_agreement.name, "Read and accept agreement", 1),
        (task_join1.name, "Skip to next action", 2))
    )
    
    return (4, wf_spec)
    
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
    cust_insurance_start = specs.Simple(wf_spec, "Start Customer Insurance section")
    cust_event_attendance_start = specs.Simple(wf_spec, "Start RAMP Section")

    #Review forms
    cust_ramp_review = AbstractForm.create_approval_wrapper(wf_spec, cust_event_attendance_start, appr_join1, 
        "Risk Assessment", task_info="""Assess the customers RAMP application in accordance with the relevant legislation and business rules (<a href=\"link.to/ramp_rules\">link</a>)""")
    cust_insure_review = AbstractForm.create_approval_wrapper(wf_spec, cust_insurance_start, appr_join1, 
    "Insurance", task_info="""Assess the customers insurance papers in accordance with the relevant legislation and business rules (<a href=\"link.to/insurance_rules\">link</a>)""")
    cust_waste_plan_review = AbstractForm.create_approval_wrapper(wf_spec, cust_waste_plan, appr_join2, 
    "Waste Plan" , task_info="""Assess the customers Waste Plan application in accordance with the relevant legislation and business rules (<a href=\"link.to/waste_rules\">link</a>)""")
    cust_traffic_plan_review = AbstractForm.create_approval_wrapper(wf_spec, cust_traffic_plan, appr_join2, 
    "Traffic Plan" , task_info="""Assess the customers Traffic Plan application in accordance with the relevant legislation and business rules (<a href=\"link.to/traffic_rules\">link</a>)""")
    #Branching taskforms
    cust_ramp_tally = CheckTally.create_exclusive_task(wf_spec, "Preliminary Risk Assessment", 40, 
                                                            cust_upload_ramp, cust_ramp_review)
    
    cust_event_attendance = ChooseBranch.create_exclusive_task(wf_spec, "Participant attendance expectation",
        (1, cust_upload_ramp),
        (2, cust_ramp_tally)
    )
                                                            
    cust_insurance_req = ChooseBranch.create_exclusive_task(wf_spec, "Event insurance requirement",
        (1, cust_upload_insure),
        (2, cust_insure_review)
    )
    
    appr_review1 = ChooseBranches.create_multichoice_task(wf_spec, 'Review and Assign Tasks',
        (1, cust_waste_plan),
        (2, cust_traffic_plan)
    )
    
    #Connections
    wf_spec.start.connect(cust_agreement)
    wf_spec.start.connect(appr_agreement)
    
    cust_agreement.connect(cust_event_info)
    
    cust_event_info.connect(cust_event_attendance_start)
    cust_event_attendance_start.connect(cust_event_attendance)
    cust_event_info.connect(cust_insurance_start)
    cust_insurance_start.connect(cust_insurance_req)
    cust_upload_insure.connect(cust_insure_review)
    cust_upload_ramp.connect(cust_ramp_review)
    appr_join1.connect(appr_review1)
    appr_join1.connect(appr_join2)
    cust_waste_plan.connect(cust_waste_plan_review)
    cust_traffic_plan.connect(cust_traffic_plan_review)
    
    #S1: Agreement acceptance
    cust_agreement.set_data(task_data = AcceptAgreement.make_task_dict(True, cust_agreement_text, 'CUSTOMER'))
    appr_agreement.set_data(task_data = AcceptAgreement.make_task_dict(True, appr_agreement_text, 'APPROVER'))

    #S2: Event Info form
    cust_event_info.set_data(task_data = FieldEntry.make_task_dict('CUSTOMER',
        ('event_name', "What is the name of your proposed event", 'text', True),
        ('event_description', "Please describe the nature of your event", 'text', True),
        ('info_first_event', "Is this the first time you've organised an event?" , 'checkbox', False),
        ('event_other', "Please enter any relevant comments about your event", 'text', False),
        task_info="""Welcome to the <b>DigiApproval</b> system. 
If you have any concern during your application process please contact your assigned assessor."""
    ))
    cust_event_attendance.set_data(task_data = ChooseBranch.make_task_dict('CUSTOMER',
        (cust_upload_ramp.name, "Over 50 participants are expected to attend", 1),
        (cust_ramp_tally.name, "Fewer than 50 participants are expected to attend ", 2),
        task_info="""In order to assess your need for a <b>Risk Assessment Management Plan</b> (RAMP) we require some information on the number of expected attendies."""
    ))
    cust_ramp_tally.set_data(task_data = CheckTally.make_task_dict('CUSTOMER',
        ('large_structures', "Will there be large structures at your event", False, 10),
        ('electircal_equipment', "Will there be electrical cabling", False, 20),
        ('water_hazards', "Will there be bodies of water at your event", False, 15),
        ('hazardous_materials', "Does your event involve hazardous materials ", False, 41),
        task_info="""In order to assess your need for a <b>Risk Assessment Management Plan</b> (RAMP) we require some information on the nature of your event."""
    ))
    cust_upload_ramp.set_data(task_data = FileUpload.make_task_dict(True, 'CUSTOMER',
        task_info="""Please upload a completed <b>Risk Assessment Management Plan</b> (RAMP). 
A template can be found on the DigiApproval website (<a href=\"link.to/ramp_template\">link</a>)"""))    
    cust_insurance_req.set_data(task_data = ChooseBranch.make_task_dict('CUSTOMER',
        (cust_upload_insure.name, "My event falls under the requirements of public liability insurance", 1),
        (cust_insure_review.name, "My event does not fall under the requirements of Public Liability Insurance",2),
        task_info="""Some events require the holding of Public Liability Insurance. If you are unsure about if it is required for your event, please refer to our help page (<a href=\"link.to/insurance_help\">link</a>)"""
    ))
    cust_upload_insure.set_data(task_data = FileUpload.make_task_dict(True, 'CUSTOMER'),
        task_info="""Please upload proof of your <b>Public Liability Insurance</b> for this event. 
If you need assistance applying for cover, please refer to our help page (<a href=\"link.to/insurance_help\">link</a>)"""
    )
    
    #S3: Approval stage
    appr_review1.set_data(task_data = ChooseBranches.make_task_dict('APPROVER', 0,
        (cust_waste_plan.name, "Assign Waste Management Plan", 1),
        (cust_traffic_plan.name, "Assign Traffic Management Plan", 2),
        task_info = """Please review the previously completed stages and, if appropriate, assign further tasks for the customer to complete"""
        
    ))    
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
    
    return (5, wf_spec)

#Dummy text for agreements    
lorum_ipsum = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer sollicitudin ultrices elementum. Nam vel luctus tortor. Sed pretium sodales dui. Nullam id ante a metus ultricies sagittis. Vestibulum porttitor pretium imperdiet. Curabitur dolor est, euismod quis tellus a, volutpat scelerisque felis. Sed ac venenatis libero. Fusce quis tortor nec arcu malesuada faucibus sed at tellus. Fusce a consectetur magna. Integer ullamcorper sollicitudin ligula. Donec interdum luctus nisl ac eleifend. Nunc lobortis quam non nisl laoreet, quis fermentum elit sagittis.

Maecenas lobortis pretium volutpat. Phasellus et arcu aliquet purus varius tincidunt. Integer a libero turpis. Nunc iaculis orci et gravida auctor. Etiam feugiat porta orci a auctor. Sed sagittis semper fringilla. In non dapibus augue, id pharetra eros. Suspendisse felis neque, posuere et lobortis eget, tempus vel leo. Proin suscipit justo id eros rhoncus molestie. Sed dignissim sagittis diam eu mattis. Donec vestibulum mauris in massa pulvinar pretium at blandit nunc. Sed placerat eros metus, ac interdum ante sagittis sed. Nulla pretium convallis sapien, nec accumsan urna pharetra ac.

Pellentesque ullamcorper scelerisque justo et sagittis. Sed tempor nisl at purus luctus, a fermentum libero condimentum. Cras eu nibh porta, venenatis ligula eget, auctor lacus. Etiam eu aliquam sapien. Fusce nisi sapien, aliquam elementum odio vel, lacinia facilisis eros. Nam lacinia sed risus bibendum convallis. Curabitur blandit libero et mi aliquet, tincidunt lacinia elit pellentesque. Maecenas ultrices quis lacus ac egestas. Praesent eu elementum arcu.

Vivamus condimentum sapien non ultrices interdum. Nullam dignissim, elit quis consectetur convallis, dui ipsum commodo lorem, sit amet eleifend lectus lacus non eros. Etiam dapibus elit et enim viverra commodo. Pellentesque sit amet imperdiet massa, vitae aliquet augue. Proin lacinia egestas diam eu mattis. Vestibulum pretium lobortis lectus, a scelerisque risus pretium at. Cras malesuada sapien eu mauris suscipit lacinia. Phasellus et accumsan lorem, interdum pretium neque. Curabitur magna nibh, sollicitudin at magna at, rhoncus fringilla quam. Vivamus nec accumsan est. Maecenas hendrerit ut sapien eu auctor.

Morbi imperdiet mauris et mi suscipit tempor. Aenean congue risus ac ante aliquet interdum. Integer metus ligula, luctus vel nisi sed, blandit varius elit. Nam et purus quis tortor faucibus faucibus et quis ipsum. In nibh orci, pretium nec elementum at, malesuada eget ligula. Phasellus imperdiet tempus hendrerit. Sed ut sollicitudin augue, eu molestie mauris. In consequat aliquet dui vitae vulputate. Aliquam vitae dolor a sapien cursus sagittis in vitae magna. Fusce rutrum arcu a eros facilisis sodales. """

cust_agreement_text = """By accepting this agreement you acknowledge your reading and acceptance of both the ACT Government Acceptable Use of ICT Resources Policy and DigiApproval Fair Use agreement. Any information you provide throughout the application process is true and correct to the best of your knowledge. This service provides no warranty with regards to your application process."""

appr_agreement_text = """By accepting this agreement you acknowledge your reading and acceptance of both the ACT Government Acceptable Use of ICT Resources Policy and DigiApproval Fair Use agreement. Any information you provide throughout the application process is true and correct to the best of your knowledge. You agree to assess this application with complete impartiality and in accordance with the relevant legislation and business rules. This service provides no warranty with regards to your application process."""   


