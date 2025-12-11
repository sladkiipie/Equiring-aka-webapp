from django.urls import path
from . import views
from .views import set_password_view

urlpatterns = [
    path('', views.home_page, name='home'), # Домка
    path('create-primary-user', views.create_primary_user, name='create-primary-user'),
    path('set-passeord/<uuid:token>', set_password_view, name='login_reg'),
    path('create-contract/', views.create_contract, name='create_contract'),
    path('create-ticket/', views.create_ticket, name='create_ticket'),
    path('contracts/', views.contract_page, name='contracts_page'), # Контракты юзера - СПИСОК
    path('tickets/', views.ticket_page, name='ticket_page'),  # Тикеты юзера - СПИСОК
    path('help/', views.create_ticket, name='create_ticket'), # ПОДДЕРЖКА - ОБРАЩЕНИЕ НА ФОРМУ ПОДДЕРЖКИ
    path('login-page/', views.login_page, name='loginpage'),
    path('logout/', views.logout, name='logout'),

]
