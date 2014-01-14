from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login
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
    
def login_customer(request):
    """login controler for customer accounts"""
    if request.method == 'POST':
        login_form = LoginCustomerForm(request.POST)
        user = login_form.is_valid()
        if user is not None:
            login(request, user)
            return index(request)
    else:
        login_form = LoginCustomerForm()
    return render(request, 'digiapproval/login_customer.html', {
        'form' : login_form,
    })
    
def logout(request):
    from django.contrib.auth import logout as auth_logout
    if request.user.is_authenticated():
        auth_logout(request)
    return index(request)
            
