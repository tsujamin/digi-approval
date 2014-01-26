from django import forms
from django.forms.formsets import BaseFormSet
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import models

class RegisterCustomerForm(forms.Form):
    """User registration for for use by DigiApproval customers"""
    type = forms.ChoiceField(
        label = 'Account Type',
        choices = models.CustomerAccount.ACCOUNT_TYPE_CHOICES,
    )
    username = forms.CharField(
        label = 'Username',
        max_length = 30,
        min_length = 5,
    )
    email = forms.EmailField(
        label = 'Email',
    )
    password = forms.CharField(
        label = 'Password',
        max_length = 20,
        min_length = 5,
        widget = forms.PasswordInput(),
    )
    password_confirm = forms.CharField(
        label = 'Confirm Password',
        max_length = 20,
        min_length = 5,
        widget = forms.PasswordInput(),
    )
    
    def is_valid(self): #errors not displayed
        """Check form for valid passwords and available usernames"""
        valid = True
        if not super(RegisterCustomerForm, self).is_valid():
            return False
        if User.objects.filter(username=self.cleaned_data['username'].lower()).count() is not 0:
            self._errors['user_taken'] = "User name already exists"
            valid = False
        if User.objects.filter(email=self.cleaned_data['email'].lower()).count() is not 0:
            self._errors['email_taken'] = "Email already registered"
            valid = False
        if self.cleaned_data['password'] != self.cleaned_data['password_confirm']:
            self._errors['missmatching_passwords'] = "Passwords do not match"
            valid = False
        return valid
    
    def create_customer(self):
        """returns CustomerAccount created from self form"""
        user = User.objects.create_user(self.cleaned_data['username'], 
                    self.cleaned_data['email'], 
                    self.cleaned_data['password'],
        )
        user.save()
        account = models.CustomerAccount(user=user,
            account_type = self.cleaned_data['type'],
        )
        account.save()
        return account
        
class LoginForm(forms.Form):
    """Simple login form for accounts"""
    username = forms.CharField(
        label = 'Username',
        max_length = 30,
        min_length = 5,
    )
    password = forms.CharField(
        label = 'Password',
        max_length = 20,
        min_length = 5,
        widget = forms.PasswordInput(),
    )
    
    def is_valid(self): #doesnt render errors
        """Checks for valid user and returns it if authentication is successful"""
        if super(LoginForm, self).is_valid():
            user = authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
            if user is not None and user.is_active:
                return user
            else:
                self._errors['bad_combination'] = "Invalid username/password combination"
        return None

           
class DelegatorForm(forms.Form):
    """Form for delegator to change workflow's approver"""
    
    def __init__(self, approvers, *args, **kwargs):
        super(DelegatorForm, self).__init__(*args, **kwargs)
        self.approver = forms.ChoiceField(choices=approvers)
        
class DelegatorFormSet(BaseFormSet):
    """Formset to populate DelegatorForms with appropriate choices
    
    See https://djangosnippets.org/snippets/1863/"""
    
    def __init__(self, *args, **kwargs):
        self.approvers = kwargs.pop('approvers', None)
        super(DelegatorFormSet, self).__init__(*args, **kwargs) # this calls _construct_forms()

    def _construct_forms(self):
        # this one is merely taken from Django's BaseFormSet
        # except the additional approvers parameter for the form constructor
        self.forms = []
        for i in xrange(self.total_form_count()):
            self.forms.append(self._construct_form(i, approvers=self.approvers))    
    
            
            
        
    
    
        
    
    