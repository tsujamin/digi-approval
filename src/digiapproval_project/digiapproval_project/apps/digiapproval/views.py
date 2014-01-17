from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from .forms import *
import models

def index(request):
    
    return HttpResponse("DigiApproval 2014, welcome " + request.user.username.title())

def register_customer(request):
    """Creates CustomerUser and corresponding User if RegisterUserForm is valid"""
    if request.method == 'POST':
        form = RegisterCustomerForm(request.POST)
        if form.is_valid():
            account = form.create_customer()
            if account is not None:
                return HttpResponse("Account Successfully Created")
    else:
        form = RegisterCustomerForm()
    return render(request, 'digiapproval/register_customer.html', {
        'form' : form,
    })
    
def login(request):
    """Login controller for customer accounts, Currently doesnt display error on bad credentials"""
    from django.contrib.auth import login as auth_login
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        user = login_form.is_valid()
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect(reverse('index'))
    else:
        login_form = LoginForm()
    return render(request, 'digiapproval/login.html', {
        'form' : login_form,
    })
    
def logout(request):
    """Logs out any currently logged in user"""
    from django.contrib.auth import logout as auth_logout
    if request.user.is_authenticated():
        auth_logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required()
def modify_subaccounts(request):
    """ Controller for modify_subaccounts template. Requires an authenticated CustomerAccount of type ORGINISATION
        Currently doesnt return useful error messages """
    try:
        customer = request.user.customeraccount
    except: #Not a customeraccount
        return HttpResponseRedirect(reverse('index'))
    if customer.account_type != 'ORGANISATION' or not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))
        
    if request.method == 'POST':
        if request.POST.get('remove_account', False):
            customer.sub_accounts.remove(
                models.CustomerAccount.objects.get(id=request.POST['remove_account']))
        elif request.POST.get('add_account', False):
            try:
                customer.sub_accounts.add(
                    models.CustomerAccount.objects
                        .filter(user__username=request.POST['add_account'], account_type='CUSTOMER')[0])
            except:
                pass
        customer.save()    
    return render(request, 'digiapproval/modify_subaccounts.html', {
        'subaccounts' : customer.sub_accounts.all()
    })
    
@login_required()
def remove_parentaccounts(request):
    """ Controller for remove_parentaccounts template. Requires authenticated CustomerAccount of type CUSTOMER
        Currently doesnt return useful error messages"""
    try:
        customer = request.user.customeraccount
    except: #Not a customeraccount
        return HttpResponseRedirect(reverse('index'))
    if customer.account_type != 'CUSTOMER' or not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))
    
    if request.method == 'POST' and request.POST.get('remove_account', False):
        customer.parent_accounts.remove(
            models.CustomerAccount.objects.get(id=request.POST['remove_account']))
        customer.save()
                
    return render(request, 'digiapproval/remove_parentaccounts.html', {
        'parentaccounts' : customer.parent_accounts.all()
    })
        
    

    
    
    
    
            
