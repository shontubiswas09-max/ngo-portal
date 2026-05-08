from django.shortcuts import render
from .models import Donor

def donor_list(request):
    donors = Donor.objects.all()
    return render(request, 'donors/donor_list.html', {'donors': donors})

def add_donor(request):
    return render(request, 'donors/add_donor.html')