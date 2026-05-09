from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.report_list, name='report_list'),
    path('add/', views.add_report, name='add_report'),
    path('edit/<int:pk>/', views.edit_report, name='edit_report'),
    path('<int:pk>/', views.report_detail, name='report_detail'),
]