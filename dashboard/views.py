from django.shortcuts import render
from django.db.models import Count
from projects.models import Donor, Donation
from beneficiaries.models import Beneficiary

def dashboard_view(request):
    # Charts data
    donor_data = list(Donor.objects.annotate(
        donation_count=Count('donation')
    ).values('name', 'donation_count')[:5])

    # Literacy level data instead of gender
    literacy_data = list(Beneficiary.objects.values('literacy_level').annotate(
        count=Count('id')
    ).values('literacy_level', 'count'))

    context = {
        'donor_data': donor_data,
        'literacy_data': literacy_data,
    }
    return render(request, 'dashboard/index.html', context)