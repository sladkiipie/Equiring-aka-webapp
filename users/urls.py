from django.urls import path
from . import views
from .views import set_password_view

urlpatterns = [
    path('', views.home_page, name='home'), # Домка
    path('contracts/', views.contract_page, name='contracts'), # Контракты юзера - СПИСОК
    path('support/', views.create_ticket, name='support'), # ПОДДЕРЖКА - ОБРАЩЕНИЕ НА ФОРМУ ПОДДЕРЖКИ
    path('tickets/', views.ticket_page, name='tickets'), # Тикеты юзера - СПИСОК
    path('set-passord/<uuid:token>', set_password_view, name='set_password'),
]
