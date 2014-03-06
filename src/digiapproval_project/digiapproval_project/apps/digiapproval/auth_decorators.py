"""This module contains a selection of authentication checking function decorators.
These are used throughout the project to do role based/membership based authorisation
of users and requests.

For consistancy and maintanablility: all views/controllers requiring authentication should make use of these.

"""
from django.contrib.auth.decorators import user_passes_test, \
    REDIRECT_FIELD_NAME


def login_required_customeraccount(function=None,
                                   redirect_field_name=REDIRECT_FIELD_NAME,
                                   login_url=None):
    """
    Decorator for views that checks that the user is logged in, and that
    the user holds a CustomerAccount. Redirects to login page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and hasattr(u, 'customeraccount'),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def login_required_customer(function=None,
                            redirect_field_name=REDIRECT_FIELD_NAME,
                            login_url=None):
    """
    Decorator for views that checks that the user is logged in, and that
    the user holds a CustomerAccount of type CUSTOMER.
    Redirects to login page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: (u.is_authenticated and hasattr(u, 'customeraccount') and
                   u.customeraccount.account_type == 'CUSTOMER'),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def login_required_organisation(function=None,
                                redirect_field_name=REDIRECT_FIELD_NAME,
                                login_url=None):
    """
    Decorator for views that checks that the user is logged in, and that
    the user holds a CustomerAccount of type ORGANISATION.
    Redirects to login page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: (u.is_authenticated and hasattr(u, 'customeraccount') and
                   u.customeraccount.account_type == 'ORGANISATION'),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def login_required_approver(function=None,
                            redirect_field_name=REDIRECT_FIELD_NAME,
                            login_url=None):
    """
    Decorator for views that checks that the user is logged in, and that
    the user is an approver for at least one WorkflowSpec.
    Redirects to login page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: (u.is_authenticated and
                   any([g.workflowspecs_approvers.all()
                        for g in u.groups.all()
                        if hasattr(g, 'workflowspecs_approvers')])),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def login_required_delegator(function=None,
                             redirect_field_name=REDIRECT_FIELD_NAME,
                             login_url=None):
    """
    Decorator for views that checks that the user is logged in, and that
    the user is a delegator for at least one WorkflowSpec.
    Redirects to login page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: (u.is_authenticated and
                   any([g.workflowspecs_delegators.all()
                        for g in u.groups.all()
                        if hasattr(g, 'workflowspecs_delegators')])),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def login_required_super(function=None,
                         redirect_field_name=REDIRECT_FIELD_NAME,
                         login_url=None):
    """Decorator for views that checks if the user is authenticated as a
    superuser"""
    actual_decorator = user_passes_test(
        lambda u: (u.is_authenticated and
                   u.is_superuser),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
