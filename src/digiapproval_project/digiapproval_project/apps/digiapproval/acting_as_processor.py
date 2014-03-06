"""Context processor to handle the acting_as functionality."""

from django.core.exceptions import PermissionDenied
from .models import CustomerAccount


def acting_as(request):
    """ Context processor to handle the 'acting_as' functionality of
        CustomerAccounts with parent accounts.
    """
    result = {'acting_as': {'name': None,
                            'others': []}}

    acting_as_id = request.session.get('acting_as_id', None)
    if acting_as_id is None:
        return result

    # check we're logged in as a customer: approvers can't act as.
    try:
        customer = request.user.customeraccount
    except:  # todo fixme tighten
        return result

    # check for funny business
    if not customer.can_i_act_as_user_id(acting_as_id):
        # the only way this can happen is if someone is twiddling
        # sessions. They shouldn't be doing that.
        raise PermissionDenied

    # fill in the data
    acting_as = CustomerAccount.objects.get(id=int(acting_as_id))
    result['acting_as']['name'] = acting_as.user.get_full_name()

    others = [customer]
    others.extend([x for x in customer.parent_accounts.all()])
    others.remove(acting_as)
    result['acting_as']['others'] = [(x.id, x.user.get_full_name())
                                     for x in others]

    return result
