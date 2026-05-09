from django.urls import path
from . import views

app_name = 'donors'

urlpatterns = [
    path('', views.donor_list, name='donor_list'),
    path('add/', views.add_donor, name='add_donor'),
    path('edit/<int:pk>/', views.edit_donor, name='edit_donor'),
    path('<int:pk>/', views.donor_detail, name='donor_detail'),
]