from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from supports.models import SupporTicket
from .models import User, RegistrationToken, Contracts, Companies
from .forms import TicketForm, PrimaryUserForm, SetPasswordForm, CreateContractForm, CreateCompanyForm




def home_page(request):
    return redirect(request, 'support/home.html')

def login_page(request): #проверяет авторизован ли пользователь, если да то пропускает на главную страницу, если нет то открывает страницу авторизации
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
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
            return redirect('home')
        else: # если нет то ошибка
            messages.error(request, 'Ничего нет')
    context = {'page': page}
    return render(request, 'studentpages/login.html', context)

def logout_user(request):
    logout(request)
    return redirect('home') # выходит из аккаунта

def ticket_page(request):
    return redirect(request, 'ticket_page.html')

def create_ticket(request): # создает тикет с данными из формы contract description
    form = TicketForm()
    if request.method == 'POST':
        SupporTicket.objects.create(
            contract=request.POST.get('contract'),
            description=request.POST.get('description'),
        )
        context = {'form': form}
        return render(request, 'support/ticket.html', context)
    else:
        return redirect(request, 'support/ticket.html')

def contract_page(request):
    return redirect(request, 'support/contract.html') # страница контрактов

def create_primary_user(request): # создание первичной заявки на консультацию на открытие эквайринга
    form = PrimaryUserForm()
    if request.method == 'POST':
        if form.is_valid():
            User.objects.create(
                name=request.POST.get('name'),
                phone_number=request.POST.get('phone_number'),
                email=request.POST.get('email'),
                message=request.POST.get('message'),
            )
            form.save()
            return redirect(request, 'support/contract.html')
    else:
        context = {'form': form}
        return render(request, 'support/contract.html', context)

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
            return redirect('home_page')
    else:
        form = SetPasswordForm(User)

    return render(request, "users/set_password.html", {'form': form})

def create_contract(request):
    contract_form = CreateContractForm()
    company_form = CreateCompanyForm
    if request.method == 'POST':
        if company_form.is_valid() and contract_form.is_valid():
            Companies.objects.create(
                INN=request.POST.get('INN'),
                OGRN=request.POST.get('OGRN'),
                name_company=request.POST.get('name_company'),
            ),
            company_form.save()
            Contracts.objects.create(
                name_contracts=request.POST.get('name_contracts'),
            ),
            contract_form.save()

        return redirect('create_contract_page')

    else:
        context = {
            "company_form": company_form,
            "contract_form": contract_form,
        }
        return render(request, 'support/contract.html', context)

def create_another_contract(request):
    form = CreateContractForm()
    if request.method == 'POST':
        if form.is_valid():
            Contracts.objects.create(
                name_contracts=request.POST.get('name_contracts'),
            )
            form.save()
            return redirect('create_contract_page')
    else:
        context = {"form": form}
        return render(request, 'support/another_contract.html', context)