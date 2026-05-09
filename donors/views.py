from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Donor

def donor_list(request):
    donors = Donor.objects.all()
    return render(request, 'donors/donor_list.html', {'donors': donors})

@login_required(login_url='admin:login')
def add_donor(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            profile_picture = request.FILES.get('profile_picture')
            document = request.FILES.get('document')
            
            donor = Donor(
                name=name,
                email=email,
                phone=phone,
                profile_picture=profile_picture,
                document=document
            )
            donor.save()
            messages.success(request, f'Donor {name} added successfully!')
            return redirect('donors:donor_list')
        except Exception as e:
            messages.error(request, f'Error adding donor: {str(e)}')
    
    return render(request, 'donors/add_donor.html')

@login_required(login_url='admin:login')
def edit_donor(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            profile_picture = request.FILES.get('profile_picture')
            document = request.FILES.get('document')
            
            donor.name = name
            donor.email = email
            donor.phone = phone
            if profile_picture:
                donor.profile_picture = profile_picture
            if document:
                donor.document = document
            donor.save()
            messages.success(request, f'Donor {name} updated successfully!')
            return redirect('donors:donor_list')
        except Exception as e:
            messages.error(request, f'Error updating donor: {str(e)}')
    
    return render(request, 'donors/add_donor.html', {'donor': donor})

def donor_detail(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    return render(request, 'donors/donor_detail.html', {'donor': donor})