from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'projects/project_list.html', {'projects': projects})

@login_required(login_url='admin:login')
def add_project(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            description = request.POST.get('description')
            image = request.FILES.get('image')
            
            if not name:
                messages.error(request, 'Project name is required.')
                return render(request, 'projects/add_project.html')
            
            project = Project(
                name=name,
                description=description,
                image=image
            )
            project.save()
            messages.success(request, f'Project {name} added successfully!')
            return redirect('projects:project_list')
        except Exception as e:
            messages.error(request, f'Error adding project: {str(e)}')
    
    return render(request, 'projects/add_project.html')

@login_required(login_url='admin:login')
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            description = request.POST.get('description')
            image = request.FILES.get('image')
            
            if not name:
                messages.error(request, 'Project name is required.')
                return render(request, 'projects/add_project.html', {'project': project})
            
            project.name = name
            project.description = description
            if image:
                project.image = image
            project.save()
            messages.success(request, f'Project {name} updated successfully!')
            return redirect('projects:project_list')
        except Exception as e:
            messages.error(request, f'Error updating project: {str(e)}')
    
    return render(request, 'projects/add_project.html', {'project': project})
