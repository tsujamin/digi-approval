from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .forms import RegisterUserForm
import models

def index(request):
    return HttpResponse("DigiApproval 2014")

def register_customer(request):
    """Creates CustomerUser and corresponding User if RegisterUserForm is valid"""
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            account = form.create_customer()
            if account is not None:
                return HttpResponse("Account Successfully Created")
    else:
        form = RegisterUserForm()
    return render(request, 'digiapproval/register_customer.html', {
        'form' : form,
    })
