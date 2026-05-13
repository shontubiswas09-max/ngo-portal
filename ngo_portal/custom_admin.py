from django.contrib import admin
from django.contrib.admin import AdminSite
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.apps import apps

class NGOAdminSite(AdminSite):
    site_header = "Inclusive Learning Hub Administration"
    site_title = "Inclusive Learning Hub Admin"
    index_title = "Welcome to the Inclusive Learning Hub Dashboard"
    login_template = 'admin/login.html'

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        try:
            extra_context['dashboard_url'] = reverse('dashboard:index')
        except NoReverseMatch:
            extra_context['dashboard_url'] = '/dashboard/'
        return super().index(request, extra_context)

ngo_admin_site = NGOAdminSite(name='admin')

# Register all models with the custom admin site
def register_models():
    # Import models and register them
    try:
        from beneficiaries.models import Beneficiary
        from donors.models import Donor
        from projects.models import Project, Donation, Notification, Publication, Recruitment
        from reports.models import Report
        from lms.models import (
            Teacher, Course, Lesson, Quiz, Question, QuestionOption,
            QuizAttempt, Certification, CertificateIssued, Enrollment,
            GamificationPoints, PointTransaction
        )

        class BeneficiaryAdmin(admin.ModelAdmin):
            list_display = ("name", "village", "project", "literacy_level", "attendance", "courses_completed")
            search_fields = ("name", "village")
            list_filter = ("literacy_level", "project")

        class DonorAdmin(admin.ModelAdmin):
            list_display = ('name', 'organization', 'email', 'phone', 'donation_amount', 'project')
            search_fields = ('name', 'organization', 'email', 'phone')
            list_filter = ('project',)

        class ProjectAdmin(admin.ModelAdmin):
            list_display = ('name', 'description', 'image')

        class DonationAdmin(admin.ModelAdmin):
            list_display = ('donor', 'project', 'amount', 'date')

        class NotificationAdmin(admin.ModelAdmin):
            list_display = ('title', 'created_at', 'is_read')

        class PublicationAdmin(admin.ModelAdmin):
            list_display = ('title', 'published_date', 'document')

        class RecruitmentAdmin(admin.ModelAdmin):
            list_display = ('job_title', 'posted_date', 'deadline', 'document')

        class ReportAdmin(admin.ModelAdmin):
            list_display = ("module_name", "report_name", "generated_on")
            search_fields = ("module_name", "report_name")

        class TeacherAdmin(admin.ModelAdmin):
            list_display = ('user', 'specialization', 'created_at')
            search_fields = ('user__first_name', 'user__last_name', 'specialization')
            list_filter = ('created_at',)

        class CourseAdmin(admin.ModelAdmin):
            list_display = ('title', 'teacher', 'difficulty_level', 'duration_hours', 'is_active', 'created_at')
            search_fields = ('title', 'description')
            list_filter = ('difficulty_level', 'is_active', 'created_at')

        class LessonAdmin(admin.ModelAdmin):
            list_display = ('title', 'course', 'order', 'created_at')
            search_fields = ('title', 'course__title')
            list_filter = ('course', 'created_at')
            ordering = ('course', 'order')

        class QuizAdmin(admin.ModelAdmin):
            list_display = ('title', 'course', 'passing_score', 'created_at')
            search_fields = ('title', 'course__title')
            list_filter = ('course', 'passing_score', 'created_at')

        class QuestionAdmin(admin.ModelAdmin):
            list_display = ('text', 'quiz', 'question_type', 'order')
            search_fields = ('text', 'quiz__title')
            list_filter = ('question_type', 'quiz__course')
            ordering = ('quiz', 'order')

        class QuestionOptionAdmin(admin.ModelAdmin):
            list_display = ('text', 'question', 'is_correct')
            list_filter = ('is_correct',)
            search_fields = ('text', 'question__text')

        class QuizAttemptAdmin(admin.ModelAdmin):
            list_display = ('beneficiary', 'quiz', 'score', 'passed', 'attempt_number', 'attempted_at')
            search_fields = ('beneficiary__name', 'quiz__title')
            list_filter = ('passed', 'attempt_number', 'attempted_at')
            readonly_fields = ('attempted_at', 'completed_at')

        class CertificationAdmin(admin.ModelAdmin):
            list_display = ('title', 'course', 'required_quiz_score', 'created_at')
            search_fields = ('title', 'course__title')
            list_filter = ('created_at',)

        class CertificateIssuedAdmin(admin.ModelAdmin):
            list_display = ('beneficiary', 'certification', 'certificate_number', 'issued_date')
            search_fields = ('beneficiary__name', 'certification__title', 'certificate_number')
            list_filter = ('issued_date', 'certification')
            readonly_fields = ('issued_date',)

        class EnrollmentAdmin(admin.ModelAdmin):
            list_display = ('beneficiary', 'course', 'completed', 'enrolled_at', 'completion_date')
            search_fields = ('beneficiary__name', 'course__title')
            list_filter = ('completed', 'enrolled_at')
            readonly_fields = ('enrolled_at',)

        class GamificationPointsAdmin(admin.ModelAdmin):
            list_display = ('beneficiary', 'total_points', 'level', 'streak_days', 'last_activity')
            search_fields = ('beneficiary__name',)
            list_filter = ('level', 'last_activity')
            readonly_fields = ('last_activity',)

        class PointTransactionAdmin(admin.ModelAdmin):
            list_display = ('gamification', 'activity_type', 'points_earned', 'created_at')
            search_fields = ('gamification__beneficiary__name', 'activity_type')
            list_filter = ('activity_type', 'created_at')
            readonly_fields = ('created_at',)

        # Register with custom admin site
        ngo_admin_site.register(Beneficiary, BeneficiaryAdmin)
        ngo_admin_site.register(Donor, DonorAdmin)
        ngo_admin_site.register(Project, ProjectAdmin)
        ngo_admin_site.register(Donation, DonationAdmin)
        ngo_admin_site.register(Notification, NotificationAdmin)
        ngo_admin_site.register(Publication, PublicationAdmin)
        ngo_admin_site.register(Recruitment, RecruitmentAdmin)
        ngo_admin_site.register(Report, ReportAdmin)
        
        # Register LMS models
        ngo_admin_site.register(Teacher, TeacherAdmin)
        ngo_admin_site.register(Course, CourseAdmin)
        ngo_admin_site.register(Lesson, LessonAdmin)
        ngo_admin_site.register(Quiz, QuizAdmin)
        ngo_admin_site.register(Question, QuestionAdmin)
        ngo_admin_site.register(QuestionOption, QuestionOptionAdmin)
        ngo_admin_site.register(QuizAttempt, QuizAttemptAdmin)
        ngo_admin_site.register(Certification, CertificationAdmin)
        ngo_admin_site.register(CertificateIssued, CertificateIssuedAdmin)
        ngo_admin_site.register(Enrollment, EnrollmentAdmin)
        ngo_admin_site.register(GamificationPoints, GamificationPointsAdmin)
        ngo_admin_site.register(PointTransaction, PointTransactionAdmin)

    except ImportError:
        # Models not ready yet, will be registered later
        pass

# Try to register models immediately
register_models()

