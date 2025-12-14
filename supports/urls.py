from django.urls import path
from . import views

urlpatterns = [
    path('update-contract/', views.update_contract, name='update-contract'),
    path('update-ticket/', views.update_support_ticket, name='update-tickets'),
    path('primary-user-check/', views.primary_user_check, name='primary-user-check'),
    path('company-check', views.company_check, name='company-check'),
    path('contract-check', views.contract_check, name='contract-check'),
]