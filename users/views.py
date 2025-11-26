from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from supports.models import SupporTicket
from .models import User
from .forms import TicketForm




def home_page(request):
    return redirect(request, 'support/home.html')

def login_page(request): #проверяет авторизоыв ли пользователь, если да то пропускает на главную страницу, если нет то открывает страницу авторизации
    page = 'login'
    if request.user.is_authenticated: # Если авторизован перекидвыает на главную (пока указан home)
        return redirect('home')
    if request.method == 'POST':
        uslog = request.POST.get('login') # берет информацию из формы логина
        password = request.POST.get('password') # берет ифнормацию из формы пароля
        try:
            user = User.objects.get(uslog=uslog) # честно сам не пойму как и почему но я взял его из прошлого проекта мб он не правильное
        except:
            messages.error(request, 'Пусто')
        user = authenticate(request, login=uslog, password=password) #вводит данные login password
        if user is not None: # если данные есть то переводит на домашнюю страницу
            login(request, user)
            return redirect('home')
        else: # если нет то ошибка
            messages.error(request, 'Ничего нет')
    context = {'page': page}
    return redirect(request, 'studentpages/login.html', context) # в ином из всех случаях будет страница авторицации

def logout_user(request):
    logout(request)
    return redirect('home') # выходит из аккаунта

def craete_ticket(request): # создает тикет с данными из формы contract description
    form = TicketForm()
    if request.method == 'POST':
        SupporTicket.objects.create(
            contract=request.POST.get('contract'), #  берет данные
            description=request.POST.get('description'),
        )
        context = {'form': form}
        return redirect(request, 'support/ticket.html', context) # возвращает с контекстом данных
    else:
        return redirect(request, 'support/ticket.html') # возвращает на ту же страницу

def craete_contract(request):
    pass
# Пока не будет внятной инфы какую информацию надо передать нифига не будет