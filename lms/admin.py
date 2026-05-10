from django.contrib import admin
from .models import (
    Teacher, Course, Lesson, Quiz, Question, QuestionOption, 
    QuizAttempt, Certification, CertificateIssued, Enrollment, 
    GamificationPoints, PointTransaction
)

# LMS models are registered in ngo_portal.custom_admin to use the custom admin site
# No registrations here to avoid conflicts

