from django.db import models
from projects.models import Project

class Donor(models.Model):
    name = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='donors/', blank=True, null=True)
    document = models.FileField(upload_to='donors/docs/', blank=True, null=True)
    donation_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name