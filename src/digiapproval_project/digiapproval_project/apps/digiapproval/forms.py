from django import forms
from django.forms.formsets import BaseFormSet
from models import CustomerAccount
from registration.forms import RegistrationFormUniqueEmail
from django.core.validators import MinLengthValidator


class CustomerRegistrationForm(RegistrationFormUniqueEmail):
    """User registration for for use by DigiApproval customers.
    Extends the django-registration RegistrationForm to gather the extra info
    we need."""
    first_name = forms.CharField(max_length=30,
                                 validators=[MinLengthValidator(1)])
    last_name = forms.CharField(max_length=30,
                                validators=[MinLengthValidator(1)])
    type = forms.ChoiceField(
        label='Account Type',
        choices=CustomerAccount.ACCOUNT_TYPE_CHOICES,
    )


class DelegatorForm(forms.Form):
    """Form for delegator to change workflow's approver"""
    workflow_id = forms.IntegerField(widget=forms.HiddenInput)

    # required=False because we don't actually post these back
    workflow_customer = forms.CharField(widget=forms.HiddenInput,
                                        required=False)
    workflow_customer_username = forms.CharField(widget=forms.HiddenInput,
                                                 required=False)

    def __init__(self, approvers, *args, **kwargs):
        super(DelegatorForm, self).__init__(*args, **kwargs)
        self.fields['approver'] = forms.ChoiceField(choices=approvers,
                                                    widget=forms.Select(attrs={
                                                        'class': 'form-control'
                                                        }))


class DelegatorBaseFormSet(BaseFormSet):
    """Base formset to populate DelegatorForms with appropriate choices"""

    def __init__(self, *args, **kwargs):
        self.approvers = kwargs.pop('approvers', None)
        # this calls _construct_forms()
        super(DelegatorBaseFormSet, self).__init__(*args, **kwargs)

    def _construct_form(self, index, **kwargs):
        kwargs['approvers'] = self.approvers
        return super(DelegatorBaseFormSet, self)._construct_form(
            index, **kwargs)
