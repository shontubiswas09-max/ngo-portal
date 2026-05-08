from django.urls import path
from . import views

app_name = 'donors'

urlpatterns = [
    path('', views.donor_list, name='donor_list'),
    path('add/', views.add_donor, name='add_donor'),
]