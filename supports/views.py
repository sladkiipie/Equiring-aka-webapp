from django.shortcuts import redirect, render
from django.contrib import messages


from .forms import SupporTicketForm, PrimaryUserCheckForm, UpdateContractForm, CheckCompanyForm, CheckContractForm
from .models import SupporTicket

from users.models import Contracts, User, Companies


def update_support_ticket(request): # изменяет статус тикета
    try:
        support_ticket = SupporTicket.objects.get(id=id)
        form = SupporTicketForm(instance=support_ticket)
        if request.method == "POST":
            support_ticket.objects.update(
                status=request.POST['status'],
            )
            return redirect(request, 'support/ticket.html')
        else:
            context = {'form': form}
            return render(request, 'support/ticket.html', context)
    except SupporTicket.DoesNotExist:
        messages.error(request, 'Support ticket not found.')

def update_contract(request): # обновляет  информацию о контаркте ссылку на компанию, назывние контракта и файл документа
    try:
        contracts = Contracts.objects.get(id=id)
        form = UpdateContractForm(instance=contracts)
        if request.method == "POST":
            Contracts.objects.update(
                company=request.POST['company'],
                name=request.POST['name'],
                document=request.POST['document'],
            )
            return redirect(request, 'support/contracts-list.html')
        else:
            context = {'form': form}
            return render(request, 'support/contracts-list.html', context)
    except Contracts.DoesNotExist:
        messages.error(request, 'Contract not found.')

def primary_user_check(request):
    try:
        primary_user = User.objects.get(id=id)
        form = PrimaryUserCheckForm(instance=primary_user)
        if request.method == 'POST':
            User.objects.update(
                status=request.POST['status'],
            )
            return redirect(request, 'support/users-list.html')
        else:
            context = {'form': form}
            return render(request, 'support/users-list.html', context)
    except User.DoesNotExist:
        messages.error(request, 'User not found')

def company_check(request):
    try:
        company = Companies.objects.get(id=id)
        form = CheckCompanyForm(instance=company)
        if request.method == 'POST':
            Companies.objects.update(
                status=request.POST['status'],
            )
            return redirect(request, 'support/companies-list.html')
        else:
            context = {'form': form}
            return render(request, 'support/companies-list.html', context)
    except Companies.DoesNotExist:
        messages.error(request, 'Company not found')

def contract_check(request):
    try:
        contract = Contracts.objects.get(id=id)
        form = CheckContractForm(instance=contract)
        if request.method == 'POST':
            if form.is_valid():
                Contracts.objects.update(
                    status=request.POST['status'],
                ),
                form.save()
                return redirect(request, 'support/contracts-list.html')
        else:
            context = {'form': form}
            return render(request, 'support/contracts-list.html', context)
    except Contracts.DoesNotExist:
        messages.error(request, 'Contract not found')
