from digiapproval_project.apps.digiapproval import models, taskforms
from django.contrib.auth.models import User, Group

#Tuple map functions
def directorate_to_group(group_name):
    group = Group(group_name)
    group.save()
    return group
    
def approver_to_user((name, password, email, groups)):
    user = User.objects.create_user(email, email, password)
    user.first_name, user.last_name = name.split()
    user.save()
    for group in groups:
        user.groups.add(group)
    return user
    
def to_customer_account((account_type, username, password, email, parents)):
    user = User.objects.create_user(username, email, password)
    user.save()
    customer = models.Customer(account_type = account_type, user = user)
    customer.save()
    for parent in parents:
        customer.parent_accounts.add(parent)
    return customer
    
#Clear current data from tables
for user in User.objects.exclude(username='super'):
    user.delete()
for group in Group.objects.all():
    group.delete()
for models in [models.Task, models.Workflow, models.WorkflowSpec, models.CustomerAccount, models.UserFile]:
    for instance in models:
        instance.delete()

DIRECTORATES = map(directorate_to_group, [ 
    'TAMS', 
    'NCA',
])


APPROVERS = map(approver_to_user, [
    ('David Potter', 'harrysorrydavid', 'David.Potter@act.gov.au', [DIRECTORATES[0]]),
    ('Cal McGregor', 'alwaystheminister', 'Cal.McGregor@act.gov.au', [DIRECTORATES[0]]),
    ('Claudia Marshall', 'neverthetwotermer', 'Claudia.Marshall@nca.gov.au', [DIRECTORATES[0], DIRECTORATES[1]]),
])

ORGANISATIONS= map(to_customer_account, [
    ('ORGANISATION', 'leaky_plumbing', 'wikiwho?', 'webmaster@leakyplumbing.org.au', []),
    ('ORGANISATION', 'kirstys_short_term_loans', 'kneecaps', 'col@kirstys.net.au', []),
])

CUSTOMERS = map(to_customer_accounts, [
    ('CUSTOMER', 'cleaver_g', 'fubar', 'clever_cleaver167@yahoo.com', []),
    ('CUSTOMER', 'missy_tanner', 'harrysorryjoshua', 'missy@hotmail.com' [ORGANISATIONS[0]]),
    ('CUSTOMER', 'j_floyd', 'ihaveaguy', 'joshua.floyd@leakyplumbing.org.au', [ORGANISATIONS[0]]),
    ('CUSTOMER', 'la_hole', '5stars', 'lane_hold@laneholdings.com.au', []),

])


