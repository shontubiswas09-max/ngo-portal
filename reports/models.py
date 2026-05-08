from django.db import models

# Create your models here.
# reports/models.py
from django.db import models

class Report(models.Model):
    module_name = models.CharField(max_length=100)
    report_name = models.CharField(max_length=200)
    generated_on = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="reports/", blank=True, null=True)

    def __str__(self):
        return f"{self.module_name} - {self.report_name}"