from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from supports.models import SupporTicket
from .models import User
from .forms import TicketForm




def home_page(request):
    return redirect(request, 'support/home.html')

def login_page(request):
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
        else:
            messages.error(request, 'Ничего нет')
    context = {'page': page}
    return redirect(request, 'studentpages/login.html', context)

def logout_user(request):
    logout(request)
    return redirect('home')

def craete_ticket(request):
    form = TicketForm()
    if request.method == 'POST':
        SupporTicket.object.create(
            contact=request.POST.get('contact'),
            description=request.POST.get('description'),
        )
        context = {'form': form}
        return redirect(request, 'support/ticket.html', context)
    else:
        return redirect(request, 'support/ticket.html')

def craete_contract(request):
    pass
# Пока не будет внятной инфы какую информацию надо передать нифига не будет