from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import User, RegistrationToken
from .forms import TicketForm, PrimaryUserForm, SetPasswordForm, CreateContractForm, CreateCompanyForm



def guest_page(request):
    return render(request, 'users/mainpage.html')

def login_page(request): #проверяет авторизован ли пользователь, если да то пропускает на главную страницу, если нет то открывает страницу авторизации
    page = 'login'
    if request.user.is_authenticated:
        return redirect('userhome.html')
    if request.method == 'POST':
        uslog = request.POST.get('login')
        password = request.POST.get('password')
        try:
            user = User.objects.get(uslog=uslog)
        except:
            messages.error(request, 'Пусто')
        user = authenticate(request, login=uslog, password=password)
        if user is not None:
            login(request, user)
            return redirect('userhome.html')
        else: # если нет то ошибка
            messages.error(request, 'Ничего нет')
    context = {'page': page}
    return render(request, 'loginpage.html', context)

def create_primary_user(request): # создание первичной заявки на консультацию на открытие эквайринга
    if request.method == 'POST':
        form = PrimaryUserForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(request, 'support/mainpage.html')
    else:
        form = PrimaryUserForm()

    return render(request, 'support/mainpage.html', {'form': form})

def set_password_view(request, token): # страница создания аккаунта (логин и пароль)
    registration_token = get_object_or_404(RegistrationToken, token=token)
    if not registration_token.is_valid():
        return redirect('users/invalid_token.html')
    if request.method == 'POST':
        form = SetPasswordForm(registration_token.user)
        if form.is_valid():
            form.save()
            registration_token.used = True
            registration_token.save()
            login(request, registration_token.user)
            return redirect('loginpage.html')
    else:
        form = SetPasswordForm(User)
    return render(request, "users/set_password.html", {'form': form})



def home_page(request):
    return render(request, 'users/userhome.html')

def logout_user(request):
    logout(request)
    return redirect('home') # выходит из аккаунта



def contract_page(request):
    return render(request, 'users/contracts.html') # страница контрактов

def create_contract(request):
    if request.method == 'POST':
        contract_form = CreateContractForm(request.POST)
        if contract_form.is_valid():
            contract_form.save()
        return redirect('contracts.html')
    else:
        contract_form = CreateContractForm()
    context = {"contract_form": contract_form,}
    return render(request, 'users/contracts.html', context)



def company_page(request):
    return render(request, 'users/companies.html')

def create_company(request):
    if request.method == 'POST':
        form = CreateCompanyForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('users/contracts.html')
    else:
        form = CreateCompanyForm()
        return render(request, 'users/companyform.html', {"form": form})



def ticket_page(request):
    return render(request, 'users/tickets.html')

def create_ticket(request):# создает тикет с данными из формы contract description
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request, 'support/tickets.html')
    else:
        form = TicketForm()

    return render(request, 'support/tickets.html', {'form': form})
