from django.db import models
from beneficiaries.models import Beneficiary
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Teacher(models.Model):
    """Teacher/Mentor model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.specialization}"


class Course(models.Model):
    """Course model"""
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='courses')
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    duration_hours = models.IntegerField(validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='courses/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Lesson model for courses"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField()
    video_url = models.URLField(blank=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Quiz(models.Model):
    """Quiz model"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    passing_score = models.IntegerField(
        default=70,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Quizzes"
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Question(models.Model):
    """Question model for quizzes"""
    QUESTION_TYPES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('short_answer', 'Short Answer'),
    ]
    
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.text[:50]


class QuestionOption(models.Model):
    """Options for multiple choice questions"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return self.text


class QuizAttempt(models.Model):
    """Track quiz attempts by beneficiaries"""
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='quiz_attempts')
    score = models.IntegerField(null=True, blank=True)
    passed = models.BooleanField(default=False)
    attempt_number = models.IntegerField(default=1)
    attempted_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['quiz', 'beneficiary', 'attempt_number']
        ordering = ['-attempted_at']
    
    def __str__(self):
        return f"{self.beneficiary.name} - {self.quiz.title} (Attempt {self.attempt_number})"


class Certification(models.Model):
    """Certification model"""
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='certification')
    title = models.CharField(max_length=200)
    description = models.TextField()
    required_quiz_score = models.IntegerField(
        default=80,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title


class CertificateIssued(models.Model):
    """Track issued certificates"""
    certification = models.ForeignKey(Certification, on_delete=models.CASCADE, related_name='issued_certificates')
    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='certificates')
    issued_date = models.DateTimeField(auto_now_add=True)
    certificate_number = models.CharField(max_length=100, unique=True)
    
    class Meta:
        unique_together = ['certification', 'beneficiary']
        ordering = ['-issued_date']
    
    def __str__(self):
        return f"{self.beneficiary.name} - {self.certification.title}"


class Enrollment(models.Model):
    """Track course enrollment"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='course_enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['course', 'beneficiary']
        ordering = ['-enrolled_at']
    
    def __str__(self):
        return f"{self.beneficiary.name} - {self.course.title}"


class GamificationPoints(models.Model):
    """Track gamification points for beneficiaries"""
    ACTIVITY_TYPES = [
        ('course_completion', 'Course Completion'),
        ('quiz_passed', 'Quiz Passed'),
        ('certification', 'Certification Earned'),
        ('attendance', 'Perfect Attendance'),
        ('participation', 'Class Participation'),
    ]
    
    beneficiary = models.OneToOneField(Beneficiary, on_delete=models.CASCADE, related_name='gamification_points')
    total_points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    badges = models.TextField(default='[]')  # JSON array of earned badges
    streak_days = models.IntegerField(default=0)  # Consecutive days active
    last_activity = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Gamification Points"
    
    def __str__(self):
        return f"{self.beneficiary.name} - Level {self.level} ({self.total_points} points)"


class PointTransaction(models.Model):
    """Log point transactions"""
    gamification = models.ForeignKey(GamificationPoints, on_delete=models.CASCADE, related_name='transactions')
    activity_type = models.CharField(max_length=20, choices=GamificationPoints.ACTIVITY_TYPES)
    points_earned = models.IntegerField()
    related_object_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.gamification.beneficiary.name} - {self.activity_type} (+{self.points_earned})"
