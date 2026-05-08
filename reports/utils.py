# reports/utils.py
from reports.models import Report

def save_report(module, name, file_path=None):
    Report.objects.create(
        module_name=module,
        report_name=name,
        file=file_path
    )