from django.urls import path
from . import views

app_name = 'lms'

urlpatterns = [
    # Course URLs
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),
    
    # Lesson URLs
    path('courses/<int:course_id>/lessons/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    
    # Quiz URLs
    path('courses/<int:course_id>/quizzes/', views.quiz_list, name='quiz_list'),
    path('quizzes/<int:quiz_id>/take/', views.take_quiz, name='take_quiz'),
    path('quizzes/attempts/<int:attempt_id>/submit/', views.submit_quiz, name='submit_quiz'),
    
    # Dashboard URLs
    path('dashboard/learner/', views.learner_dashboard, name='learner_dashboard'),
    path('dashboard/gamification/', views.gamification_dashboard, name='gamification_dashboard'),
    path('dashboard/teacher/', views.teacher_dashboard, name='teacher_dashboard'),
]
