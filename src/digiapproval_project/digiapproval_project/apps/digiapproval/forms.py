from django import forms
from django.contrib.auth.models import User
import models

class RegisterUserForm(forms.Form):
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
    
    def is_valid(self):
        """Check form for valid passwords and available usernames"""
        valid = True
        if not super(RegisterUserForm, self).is_valid():
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
        user = User(username = self.cleaned_data['username'],
            email = self.cleaned_data['email'],
            password = self.cleaned_data['password'],
        )
        user.save()
        account = models.CustomerAccount(user=user,
            account_type = self.cleaned_data['type'],
        )
        account.save()
        return account

        
        
        
            
            
        
    
    
        
    
    