from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from supports.models import SupporTicket
from .models import User, Contracts
from .forms import TicketForm, PrimaryUserForm




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
    return render(request, 'studentpages/login.html', context) # в ином из всех случаях будет страница авторицации

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
        return render(request, 'support/ticket.html', context) # возвращает с контекстом данных
    else:
        return redirect(request, 'support/ticket.html') # возвращает на ту же страницу

def craete_contract_page(request):
    return redirect(request, 'support/contract.html')

def create_primary_user(request):
    form = PrimaryUserForm()
    if request.method == 'POST':
        User.objects.create(
            name=request.POST.get('name'),
            phone_number=request.POST.get('phone_number'),
            email=request.POST.get('email'),
            message=request.POST.get('message'),
        )
        return redirect(request, 'support/contract.html')
    else:
        context = {'form': form}
        return render(request, 'support/contract.html', context)

