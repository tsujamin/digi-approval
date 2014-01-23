"""Miscellaneous authentication decorators to make our lives easier.

TODO: Testing!"""

import models
from django.contrib.auth.decorators import user_passes_test, REDIRECT_FIELD_NAME

def login_required_customeraccount(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
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


def login_required_customer(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in, and that
    the user holds a CustomerAccount of type CUSTOMER. Redirects to login page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and hasattr(u, 'customeraccount') and u.customeraccount.account_type == 'CUSTOMER',
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def login_required_organisation(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in, and that
    the user holds a CustomerAccount of type ORGANISATION. Redirects to login page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and hasattr(u, 'customeraccount') and u.customeraccount.account_type == 'ORGANISATION',
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def login_required_approver(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in, and that
    the user is an approver for at least one WorkflowSpec. Redirects to login page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and any([hasattr(g, 'workflowspecs_approvers') for g in u.groups.all()]),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def login_required_delegator(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in, and that
    the user is a delegator for at least one WorkflowSpec. Redirects to login page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and any([hasattr(g, 'workflowspecs_delegators') for g in u.groups.all()]),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator