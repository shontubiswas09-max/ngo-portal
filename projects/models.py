from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='uploads/projects/images/', blank=True, null=True)

    def __str__(self):
        return self.name
    
class Donor(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='uploads/donors/', blank=True, null=True)
    document = models.FileField(upload_to='uploads/donors/docs/', blank=True, null=True)

    def __str__(self):
        return self.name


class Donation(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor.name} → {self.project.name} ({self.amount})"


class Notification(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Publication(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    document = models.FileField(upload_to='uploads/publications/')
    published_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class Recruitment(models.Model):
    job_title = models.CharField(max_length=200)
    description = models.TextField()
    posted_date = models.DateField(auto_now_add=True)
    deadline = models.DateField()
    document = models.FileField(upload_to='uploads/recruitment/', blank=True, null=True)

    def __str__(self):
        return self.job_title


generated_on = models.DateTimeField(auto_now_add=True)
# projects/models.py
