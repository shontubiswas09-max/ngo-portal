from django.shortcuts import render
from .models import Beneficiary

def beneficiary_list(request):
    beneficiaries = Beneficiary.objects.all()
    return render(request, 'beneficiaries/beneficiary_list.html', {'beneficiaries': beneficiaries})

def add_beneficiary(request):
    return render(request, 'beneficiaries/add_beneficiary.html')