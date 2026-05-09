from django.shortcuts import render, redirect
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