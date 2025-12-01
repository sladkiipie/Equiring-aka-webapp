from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    #path('contracts/', views.contracts, name='contracts'),
]