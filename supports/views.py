from django.shortcuts import redirect, render
from django.contrib import messages


from .forms import SupporTicketForm, ContractForm, PrimaryUserCheckForm
from .models import SupporTicket

from users.models import Contracts, User




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
        contracts = Contracts.object.get(id=id)
        form = ContractForm(instance=contracts)
        if request.method == "POST":
            Contracts.objects.update(
                company=request.POST['company'],
                name=request.POST['name'],
                document=request.POST['document'],
            )
            return redirect(request, 'support/contracts.html')
        else:
            context = {'form': form}
            return render(request, 'support/contracts.html', context)
    except Contracts.DoesNotExist:
        messages.error(request, 'Contract not found.')

def primary_user_check(request):
    try:
        primary_contract = Contracts.objects.get(id=id)
        form = PrimaryUserCheckForm(instance=primary_contract)
        if request.method == 'POST':
            User.objects.update(
                status=request.POST['status'],
            )
            return redirect(request, 'support/contract.html')
        else:
            context = {'form': form}
            return render(request, 'support/contract.html', context)
    except User.DoesNotExist:
        messages.error(request, 'User not found')
