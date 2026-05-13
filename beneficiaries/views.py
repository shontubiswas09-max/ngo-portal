from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Beneficiary
from .forms import BeneficiaryForm
from projects.models import Project

def beneficiary_list(request):
    beneficiaries = Beneficiary.objects.all()
    return render(request, 'beneficiaries/beneficiary_list.html', {'beneficiaries': beneficiaries})

@login_required(login_url='admin:login')
def add_beneficiary(request):
    if request.method == 'POST':
        form = BeneficiaryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Beneficiary {form.cleaned_data["name"]} added successfully!')
            return redirect('beneficiaries:beneficiary_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BeneficiaryForm()
    
    return render(request, 'beneficiaries/add_beneficiary.html', {'form': form})

@login_required(login_url='admin:login')
def edit_beneficiary(request, pk):
    beneficiary = get_object_or_404(Beneficiary, pk=pk)
    if request.method == 'POST':
        form = BeneficiaryForm(request.POST, instance=beneficiary)
        if form.is_valid():
            form.save()
            messages.success(request, f'Beneficiary {form.cleaned_data["name"]} updated successfully!')
            return redirect('beneficiaries:beneficiary_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BeneficiaryForm(instance=beneficiary)
    
    return render(request, 'beneficiaries/add_beneficiary.html', {'form': form, 'beneficiary': beneficiary})

def beneficiary_detail(request, pk):
    beneficiary = get_object_or_404(Beneficiary, pk=pk)
    return render(request, 'beneficiaries/beneficiary_detail.html', {'beneficiary': beneficiary})