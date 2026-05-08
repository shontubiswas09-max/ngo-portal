from django.urls import path
from . import views

app_name = 'beneficiaries'

urlpatterns = [
    path('', views.beneficiary_list, name='beneficiary_list'),
    path('add/', views.add_beneficiary, name='add_beneficiary'),
]