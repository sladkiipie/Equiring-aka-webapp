from django.urls import path
from . import views

urlpatterns = [
    path('',  views.getRoutes),
    path('contracts/', views.getContracts),
    path('contracts/<str:pk>/', views.getContracts),
]