from django.db import models
from django.db import models
from projects.models import Project

class Donor(models.Model):
    name = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    donation_amount = models.DecimalField(max_digits=12, decimal_places=2)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.organization}"
# Create your models here.
class Donor(models.Model):
    name = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    donation_amount = models.DecimalField(max_digits=10, decimal_places=2)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)