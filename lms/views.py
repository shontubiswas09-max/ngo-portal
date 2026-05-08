from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q, Count, Avg
from django.utils import timezone
from datetime import timedelta
import json

from beneficiaries.models import Beneficiary
from .models import (
    Course, Lesson, Quiz, Question, QuizAttempt, Enrollment,
    Certification, CertificateIssued, GamificationPoints, PointTransaction,
    Teacher
)


def course_list(request):
    """Display list of available courses"""
    courses = Course.objects.filter(is_active=True).annotate(
        student_count=Count('enrollments')
    )
    
    difficulty = request.GET.get('difficulty')
    if difficulty:
        courses = courses.filter(difficulty_level=difficulty)
    
    context = {
        'courses': courses,
        'difficulties': [('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')]
    }
    return render(request, 'lms/course_list.html', context)


def course_detail(request, course_id):
    """Display course details and enrollment"""
    course = get_object_or_404(Course, id=course_id, is_active=True)
    lessons = course.lessons.all().order_by('order')
    quizzes = course.quizzes.all()
    
    context = {
        'course': course,
        'lessons': lessons,
        'quizzes': quizzes,
        'student_count': course.enrollments.count(),
    }
    return render(request, 'lms/course_detail.html', context)


@login_required
def enroll_course(request, course_id):
    """Enroll beneficiary in a course"""
    course = get_object_or_404(Course, id=course_id)
    
    # Get beneficiary from request - you may need to adjust based on your user/beneficiary relationship
    try:
        beneficiary = Beneficiary.objects.get(user=request.user)
    except:
        return redirect('course_list')
    
    enrollment, created = Enrollment.objects.get_or_create(
        course=course,
        beneficiary=beneficiary
    )
    
    if created:
        # Initialize gamification points if not exists
        GamificationPoints.objects.get_or_create(beneficiary=beneficiary)
        return redirect('course_detail', course_id=course_id)
    
    return redirect('course_detail', course_id=course_id)


def lesson_detail(request, course_id, lesson_id):
    """Display lesson content"""
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    
    # Get all lessons for navigation
    lessons = course.lessons.all().order_by('order')
    lesson_list = list(lessons)
    current_index = lesson_list.index(lesson)
    
    next_lesson = lesson_list[current_index + 1] if current_index + 1 < len(lesson_list) else None
    prev_lesson = lesson_list[current_index - 1] if current_index > 0 else None
    
    context = {
        'course': course,
        'lesson': lesson,
        'lessons': lessons,
        'next_lesson': next_lesson,
        'prev_lesson': prev_lesson,
        'current_lesson_index': current_index + 1,
        'total_lessons': len(lesson_list)
    }
    return render(request, 'lms/lesson_detail.html', context)


def quiz_list(request, course_id):
    """Display quizzes for a course"""
    course = get_object_or_404(Course, id=course_id)
    quizzes = course.quizzes.all()
    
    context = {
        'course': course,
        'quizzes': quizzes
    }
    return render(request, 'lms/quiz_list.html', context)


@login_required
def take_quiz(request, quiz_id):
    """Take a quiz"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    try:
        beneficiary = Beneficiary.objects.get(user=request.user)
    except:
        return redirect('course_list')
    
    # Get or create quiz attempt
    attempt_number = QuizAttempt.objects.filter(
        quiz=quiz, 
        beneficiary=beneficiary
    ).count() + 1
    
    attempt = QuizAttempt.objects.create(
        quiz=quiz,
        beneficiary=beneficiary,
        attempt_number=attempt_number
    )
    
    questions = quiz.questions.all().order_by('order')
    
    context = {
        'quiz': quiz,
        'questions': questions,
        'attempt': attempt
    }
    return render(request, 'lms/take_quiz.html', context)


@require_POST
@login_required
def submit_quiz(request, attempt_id):
    """Submit quiz answers and calculate score"""
    attempt = get_object_or_404(QuizAttempt, id=attempt_id)
    
    try:
        beneficiary = Beneficiary.objects.get(user=request.user)
        if attempt.beneficiary != beneficiary:
            return JsonResponse({'error': 'Unauthorized'}, status=403)
    except:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    # Calculate score
    correct_answers = 0
    total_questions = attempt.quiz.questions.count()
    
    for question in attempt.quiz.questions.all():
        answer = request.POST.get(f'question_{question.id}')
        
        if question.question_type == 'multiple_choice':
            correct_option = question.options.filter(is_correct=True).first()
            if correct_option and answer == str(correct_option.id):
                correct_answers += 1
        elif question.question_type == 'true_false':
            if answer == 'true' or answer == 'false':
                correct_option = question.options.filter(is_correct=True).first()
                if (answer == 'true' and correct_option.text == 'True') or \
                   (answer == 'false' and correct_option.text == 'False'):
                    correct_answers += 1
    
    # Calculate percentage
    score = int((correct_answers / total_questions) * 100) if total_questions > 0 else 0
    
    # Mark quiz attempt
    attempt.score = score
    attempt.passed = score >= attempt.quiz.passing_score
    attempt.completed_at = timezone.now()
    attempt.save()
    
    # Award points if passed
    if attempt.passed:
        gamification = GamificationPoints.objects.get_or_create(
            beneficiary=beneficiary
        )[0]
        
        points = 50  # Points for passing quiz
        gamification.total_points += points
        gamification.last_activity = timezone.now()
        gamification.save()
        
        # Log transaction
        PointTransaction.objects.create(
            gamification=gamification,
            activity_type='quiz_passed',
            points_earned=points,
            related_object_id=attempt.id
        )
    
    return JsonResponse({
        'success': True,
        'score': score,
        'passed': attempt.passed,
        'passing_score': attempt.quiz.passing_score
    })


@login_required
def gamification_dashboard(request):
    """Display gamification dashboard with points and badges"""
    try:
        beneficiary = Beneficiary.objects.get(user=request.user)
    except:
        return redirect('course_list')
    
    gamification = GamificationPoints.objects.get_or_create(
        beneficiary=beneficiary
    )[0]
    
    # Get recent transactions
    transactions = gamification.transactions.all()[:10]
    
    # Calculate next level progress
    next_level_points = (gamification.level + 1) * 200
    current_level_progress = (gamification.total_points % 200) / 200 * 100
    
    # Get enrolled courses
    enrollments = beneficiary.course_enrollments.all()
    
    # Get certificates
    certificates = beneficiary.certificates.all()
    
    context = {
        'beneficiary': beneficiary,
        'gamification': gamification,
        'transactions': transactions,
        'enrollments': enrollments,
        'certificates': certificates,
        'next_level_points': next_level_points,
        'current_level_progress': current_level_progress,
        'levels': [
            {'level': 1, 'title': 'Novice', 'min_points': 0},
            {'level': 2, 'title': 'Learner', 'min_points': 200},
            {'level': 3, 'title': 'Scholar', 'min_points': 400},
            {'level': 4, 'title': 'Expert', 'min_points': 600},
            {'level': 5, 'title': 'Master', 'min_points': 800},
        ]
    }
    return render(request, 'lms/gamification_dashboard.html', context)


@login_required
def learner_dashboard(request):
    """Display learner dashboard with progress and recommendations"""
    try:
        beneficiary = Beneficiary.objects.get(user=request.user)
    except:
        return redirect('course_list')
    
    # Get enrolled courses
    enrollments = beneficiary.course_enrollments.all()
    completed_enrollments = enrollments.filter(completed=True).count()
    
    # Get quiz attempts
    quiz_attempts = beneficiary.quiz_attempts.all()
    passed_quizzes = quiz_attempts.filter(passed=True).count()
    
    # Get certificates
    certificates = beneficiary.certificates.all()
    
    # Get gamification stats
    gamification = GamificationPoints.objects.get_or_create(
        beneficiary=beneficiary
    )[0]
    
    # Calculate progress
    progress_data = {
        'total_courses': enrollments.count(),
        'completed_courses': completed_enrollments,
        'quizzes_passed': passed_quizzes,
        'certificates_earned': certificates.count(),
        'total_points': gamification.total_points,
    }
    
    context = {
        'beneficiary': beneficiary,
        'enrollments': enrollments,
        'progress_data': progress_data,
        'gamification': gamification,
        'learning_recommendation': beneficiary.learning_recommendation()
    }
    return render(request, 'lms/learner_dashboard.html', context)


def teacher_dashboard(request):
    """Display teacher dashboard with course statistics"""
    try:
        teacher = Teacher.objects.get(user=request.user)
    except:
        return redirect('course_list')
    
    courses = teacher.courses.all()
    
    # Get statistics
    stats = {
        'total_courses': courses.count(),
        'total_students': Enrollment.objects.filter(course__in=courses).count(),
        'total_quizzes': Quiz.objects.filter(course__in=courses).count(),
        'average_quiz_score': QuizAttempt.objects.filter(quiz__course__in=courses).exclude(
            score__isnull=True
        ).values('quiz__course').annotate(avg_score=models.Avg('score'))
    }
    
    context = {
        'teacher': teacher,
        'courses': courses,
        'stats': stats
    }
    return render(request, 'lms/teacher_dashboard.html', context)
