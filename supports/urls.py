from django.urls import path
from . import views

urlpatterns = [
    path('update-contract/', views.update_contract, name='update-contracts'),
    path('update-support-ticket/', views.update_support_ticket, name='update-support-tickets'),
]