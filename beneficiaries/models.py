from django.db import models
from django.contrib.auth.models import User
from projects.models import Project

class Beneficiary(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    village = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    livelihood_activity = models.CharField(max_length=200)
    literacy_level = models.CharField(
        max_length=50,
        choices=[
            ("None", "None"),
            ("Primary", "Primary"),
            ("Secondary", "Secondary"),
            ("Higher", "Higher"),
        ],
        default="None"
    )
    skills = models.TextField(blank=True)
    training_history = models.TextField(blank=True)
    attendance = models.IntegerField(default=0)  # number of sessions attended
    courses_completed = models.IntegerField(default=0)  # completed courses
    
    def __str__(self):
        return self.name
    
    def learning_recommendation(self):
        if self.literacy_level == "None":
            return "Enroll in basic literacy program."
        elif self.literacy_level == "Primary" and self.courses_completed < 2:
            return "Take foundational skill-building courses."
        elif self.attendance < 5:
            return "Increase attendance to improve learning outcomes."
        else:
            return "Eligible for advanced vocational training."
    
    class Meta:
        verbose_name_plural = "Beneficiaries"