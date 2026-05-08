# projects/views.py
from django.shortcuts import render, redirect
from .forms import ReportForm

def add_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('report_list')
    else:
        form = ReportForm()
    return render(request, 'add_report.html', {'form': form})