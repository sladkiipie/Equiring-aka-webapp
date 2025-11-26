from django.urls import path
from . import views

urlpatterns = [
    path('ticket_sup', views.ticket_sup, name='ticket_sup'), # Сапорт тикета юзера
]