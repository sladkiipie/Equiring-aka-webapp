from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'), # Домка
    path('contracts/', views.contracts, name='contracts'), # Контракты юзера - СПИСОК
    path('support/', views.support, name='support'), # ПОДДЕРЖКА - ОБРАЩЕНИЕ НА ФОРМУ ПОДДЕРЖКИ
    path('tickets/', views.tickets, name='tickets'), # Тикеты юзера - СПИСОК
]
