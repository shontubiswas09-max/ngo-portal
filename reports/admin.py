from django.contrib import admin

# Register your models here.
# reports/admin.py
from django.contrib import admin

from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("module_name", "report_name", "generated_on")
    search_fields = ("module_name", "report_name")
