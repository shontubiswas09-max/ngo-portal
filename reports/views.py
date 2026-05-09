from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Report

def report_list(request):
    reports = Report.objects.all().order_by("-generated_on")
    return render(request, "reports/report_list.html", {"reports": reports})

@login_required(login_url='admin:login')
def add_report(request):
    if request.method == 'POST':
        try:
            module_name = request.POST.get('module_name')
            report_name = request.POST.get('report_name')
            file = request.FILES.get('file')
            
            if not module_name or not report_name:
                messages.error(request, 'Module and Report name are required.')
                return render(request, 'reports/add_report.html')
            
            report = Report(
                module_name=module_name,
                report_name=report_name,
                file=file
            )
            report.save()
            messages.success(request, f'Report "{report_name}" generated successfully!')
            return redirect('reports:report_list')
        except Exception as e:
            messages.error(request, f'Error adding report: {str(e)}')
    
    return render(request, 'reports/add_report.html')

@login_required(login_url='admin:login')
def edit_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if request.method == 'POST':
        try:
            module_name = request.POST.get('module_name')
            report_name = request.POST.get('report_name')
            file = request.FILES.get('file')
            
            if not module_name or not report_name:
                messages.error(request, 'Module and Report name are required.')
                return render(request, 'reports/add_report.html', {'report': report})
            
            report.module_name = module_name
            report.report_name = report_name
            if file:
                report.file = file
            report.save()
            messages.success(request, f'Report "{report_name}" updated successfully!')
            return redirect('reports:report_list')
        except Exception as e:
            messages.error(request, f'Error updating report: {str(e)}')
    
    return render(request, 'reports/add_report.html', {'report': report})