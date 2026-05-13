from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Donor
from .forms import DonorForm
from projects.models import Project

def donor_list(request):
    donors = Donor.objects.all()
    return render(request, 'donors/donor_list.html', {'donors': donors})

@login_required(login_url='admin:login')
def add_donor(request):
    if request.method == 'POST':
        form = DonorForm(request.POST, request.FILES)
        if form.is_valid():
            donor = form.save()
            # Create donation if amount is provided
            if donor.donation_amount and donor.donation_amount > 0 and donor.project:
                from projects.models import Donation
                Donation.objects.create(
                    donor=donor,
                    project=donor.project,
                    amount=donor.donation_amount
                )
            messages.success(request, f'Donor {form.cleaned_data["name"]} added successfully!')
            return redirect('donors:donor_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DonorForm()
    
    return render(request, 'donors/add_donor.html', {'form': form})

@login_required(login_url='admin:login')
def edit_donor(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    if request.method == 'POST':
        form = DonorForm(request.POST, request.FILES, instance=donor)
        if form.is_valid():
            donor = form.save()
            # Create or update donation if amount is provided
            if donor.donation_amount and donor.donation_amount > 0 and donor.project:
                from projects.models import Donation
                # Check if donation already exists for this donor and project
                donation, created = Donation.objects.get_or_create(
                    donor=donor,
                    project=donor.project,
                    defaults={'amount': donor.donation_amount}
                )
                if not created:
                    # Update existing donation amount
                    donation.amount = donor.donation_amount
                    donation.save()
            messages.success(request, f'Donor {form.cleaned_data["name"]} updated successfully!')
            return redirect('donors:donor_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DonorForm(instance=donor)
    
    return render(request, 'donors/add_donor.html', {'form': form, 'donor': donor})

def donor_detail(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    return render(request, 'donors/donor_detail.html', {'donor': donor})

@login_required(login_url='admin:login')
def delete_donor(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    if request.method == 'POST':
        donor_name = donor.name
        donor.delete()
        messages.success(request, f'Donor {donor_name} deleted successfully!')
        return redirect('donors:donor_list')
    return render(request, 'donors/delete_donor.html', {'donor': donor})