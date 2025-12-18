from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from .models import User, RegistrationToken, Companies
from .forms import CreateTicketForm, PrimaryUserForm, SetPasswordForm, CreateContractForm, CreateCompanyForm



def guest_page(request):
    return render(request, 'users/mainpage.html')

def login_page(request): #проверяет авторизован ли пользователь, если да то пропускает на главную страницу, если нет то открывает страницу авторизации
    page = 'login'
    if request.user.is_authenticated:
        return redirect('userhome')
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
            return redirect('userhome')
        else: # если нет то ошибка
            messages.error(request, 'Ничего нет')
    context = {'page': page}
    return render(request, 'users/loginpage.html', context)

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
            return redirect('login/')
    else:
        form = SetPasswordForm(User)
    return render(request, "users/set_password.html", {'form': form})


@login_required(login_url='login')
def home_page(request):
    return render(request, 'users/userhome.html')

@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('home/') # выходит из аккаунта


@login_required(login_url='login')
def contract_page(request):
    return render(request, 'users/contracts.html') # страница контрактов

@login_required(login_url='login')
def create_contract(request):
    if request.method == 'POST':
        form = CreateContractForm(request.POST or None, user=request.user)
        if form.is_valid():
            form.save()
        return redirect('contracts')
    else:
        form = CreateContractForm(user=request.user)
    return render(request, 'users/contractform.html', {"form": form})


@login_required(login_url='login')
def company_page(request):
    return render(request, 'users/companies.html')

@login_required(login_url='login')
def create_company(request):
    if request.method == 'POST':
        form = CreateCompanyForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('companies/')
    else:
        form = CreateCompanyForm()
    return render(request, 'users/companyform.html', {"form": form})


@login_required(login_url='login')
def ticket_page(request):
    return render(request, 'users/tickets.html')

@login_required(login_url='login')
@permission_required('core.view_ticket')
def create_ticket(request):# создает тикет с данными из формы contract description
    if request.method == 'POST':
        form = CreateTicketForm(request.POST or None, user=request.user)
        if form.is_valid():
            form.save()
        return redirect(request, 'tickets/')
    else:
        form = CreateTicketForm(user=request.user)

    return render(request, 'users/supticketform.html', {'form': form})

@login_required(login_url='login')

def applications_list(request):
    return render(request, 'users/applicationslist.html')

@login_required(login_url='login')
def application_page(request):
    return render(request, 'users/applications.html')

@login_required(login_url='login')
def create_application(request):
    if request.method == 'POST':
        form = CreateTicketForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request, 'applications/')
    else:
        form = CreateTicketForm()

    return render(request, 'users/applicationform.html', {'form': form})




def user_login(request)




def user_gains_perms(request, user_id):
    content_type = content_type.objects.get_for_model(CreateContractForm)
    permission = permission.objects.get(
        codename='create_contract',
        content_type=content_type,
    )
    User.user_permissions.add(permission)
    
    
def support_perms(request):
    content_type = content_type.objects.get_for_model(CreateTicketForm)
    permission = permission.objects.get(
    codename='create_contract',
    content_type=content_type,
    )
    User.user_permissions.add(permission)
    
def client_perms(request)
    