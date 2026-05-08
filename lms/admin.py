from django.contrib import admin
from .models import (
    Teacher, Course, Lesson, Quiz, Question, QuestionOption, 
    QuizAttempt, Certification, CertificateIssued, Enrollment, 
    GamificationPoints, PointTransaction
)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'specialization')
    list_filter = ('created_at',)


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ('title', 'order', 'content', 'video_url')


class QuizInline(admin.TabularInline):
    model = Quiz
    extra = 1
    fields = ('title', 'passing_score')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'difficulty_level', 'duration_hours', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('difficulty_level', 'is_active', 'created_at')
    inlines = [LessonInline, QuizInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'teacher', 'image')
        }),
        ('Course Details', {
            'fields': ('difficulty_level', 'duration_hours', 'is_active')
        }),
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'created_at')
    search_fields = ('title', 'course__title')
    list_filter = ('course', 'created_at')
    ordering = ('course', 'order')


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    fields = ('text', 'question_type', 'order')


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'passing_score', 'created_at')
    search_fields = ('title', 'course__title')
    list_filter = ('course', 'passing_score', 'created_at')
    inlines = [QuestionInline]


class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption
    extra = 1
    fields = ('text', 'is_correct')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'question_type', 'order')
    search_fields = ('text', 'quiz__title')
    list_filter = ('question_type', 'quiz__course')
    inlines = [QuestionOptionInline]
    ordering = ('quiz', 'order')


@admin.register(QuestionOption)
class QuestionOptionAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    list_filter = ('is_correct',)
    search_fields = ('text', 'question__text')


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('beneficiary', 'quiz', 'score', 'passed', 'attempt_number', 'attempted_at')
    search_fields = ('beneficiary__name', 'quiz__title')
    list_filter = ('passed', 'attempt_number', 'attempted_at')
    readonly_fields = ('attempted_at', 'completed_at')


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'required_quiz_score', 'created_at')
    search_fields = ('title', 'course__title')
    list_filter = ('created_at',)


@admin.register(CertificateIssued)
class CertificateIssuedAdmin(admin.ModelAdmin):
    list_display = ('beneficiary', 'certification', 'certificate_number', 'issued_date')
    search_fields = ('beneficiary__name', 'certification__title', 'certificate_number')
    list_filter = ('issued_date', 'certification')
    readonly_fields = ('issued_date',)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('beneficiary', 'course', 'completed', 'enrolled_at', 'completion_date')
    search_fields = ('beneficiary__name', 'course__title')
    list_filter = ('completed', 'enrolled_at')
    readonly_fields = ('enrolled_at',)


@admin.register(GamificationPoints)
class GamificationPointsAdmin(admin.ModelAdmin):
    list_display = ('beneficiary', 'total_points', 'level', 'streak_days', 'last_activity')
    search_fields = ('beneficiary__name',)
    list_filter = ('level', 'last_activity')
    readonly_fields = ('last_activity',)


@admin.register(PointTransaction)
class PointTransactionAdmin(admin.ModelAdmin):
    list_display = ('gamification', 'activity_type', 'points_earned', 'created_at')
    search_fields = ('gamification__beneficiary__name', 'activity_type')
    list_filter = ('activity_type', 'created_at')
    readonly_fields = ('created_at',)
