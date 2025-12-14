from django.urls import path
from . import views




urlpatterns = [
    path(r'', views.home_page, name='home'), # Домка

    path('create-primary-user', views.create_primary_user, name='create-primary-user'),
    path('set-password/<uuid:token>', views.set_password_view, name='login_reg'),

    path('contracts/', views.contract_page, name='contracts'), # Контракты юзера - СПИСОК
    path('contractform/', views.contractform_page, name='contractform'),
    path('create-contract/', views.create_contract, name=''),

    path('tickets/', views.ticket_page, name='tickets'),  # Тикеты юзера - СПИСОК
    path('create-ticket/', views.create_ticket, name='create_ticket'),

    path('login/', views.login_page, name='loginpage'),
    path('logout/', views.logout, name='logout'),

]
