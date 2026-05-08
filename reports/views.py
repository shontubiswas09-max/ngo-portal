from django.shortcuts import render

# Create your views here.
# reports/views.py
from django.shortcuts import render
from .models import Report

def report_list(request):
    reports = Report.objects.all().order_by("-generated_on")
    return render(request, "reports/report_list.html", {"reports": reports})

def add_report(request):
    return render(request, 'reports/add_report.html')