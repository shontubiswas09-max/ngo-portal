from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Beneficiary

def beneficiary_list(request):
    beneficiaries = Beneficiary.objects.all()
    return render(request, 'beneficiaries/beneficiary_list.html', {'beneficiaries': beneficiaries})

@login_required(login_url='admin:login')
def add_beneficiary(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            village = request.POST.get('village')
            project_id = request.POST.get('project')
            livelihood_activity = request.POST.get('livelihood_activity')
            literacy_level = request.POST.get('literacy_level')
            skills = request.POST.get('skills')
            training_history = request.POST.get('training_history')
            
            if not name or not village or not project_id:
                messages.error(request, 'Please fill in all required fields.')
                return render(request, 'beneficiaries/add_beneficiary.html')
            
            from projects.models import Project
            project = Project.objects.get(id=project_id)
            
            beneficiary = Beneficiary(
                name=name,
                village=village,
                project=project,
                livelihood_activity=livelihood_activity,
                literacy_level=literacy_level,
                skills=skills,
                training_history=training_history
            )
            beneficiary.save()
            messages.success(request, f'Beneficiary {name} added successfully!')
            return redirect('beneficiaries:beneficiary_list')
        except Exception as e:
            messages.error(request, f'Error adding beneficiary: {str(e)}')
    
    from projects.models import Project
    projects = Project.objects.all()
    return render(request, 'beneficiaries/add_beneficiary.html', {'projects': projects})