from django.core.exceptions import PermissionDenied


def workflow_actor_type(user, workflow):
    """Identifies if the user account is the CUSTOMER or APPROVER of a
    workflow. Raises a PermssionDenied if the user is neither."""

    try:
        customer = user.customeraccount
        actor = 'CUSTOMER'
        # FIXME: this doesn't cope with multiple layers of parent account - but
        # we should probably remove those multiple layers
        if customer != workflow.customer and \
                workflow.customer not in customer.parent_accounts.all():
            raise PermissionDenied
    except:
        actor = 'APPROVER'
        if user != workflow.approver:
            raise PermissionDenied

    return actor
