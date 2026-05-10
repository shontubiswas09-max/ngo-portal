from django.urls import path
from django.views.generic import RedirectView
from .views import dashboard_view

app_name = 'dashboard'

urlpatterns = [
    path('', dashboard_view, name='index'),
    path('gamification/', RedirectView.as_view(pattern_name='lms:gamification_dashboard', permanent=False), name='gamification'),
]