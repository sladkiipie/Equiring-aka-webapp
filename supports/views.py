from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages


from .forms import SupporTicketForm, PrimaryUserCheckForm, UpdateContractForm, CheckCompanyForm, CheckContractForm
from .models import SupporTicket

from users.models import Contracts, User, Companies


def update_support_ticket(request, id):  # изменяет статус тикета

    support_ticket = get_object_or_404(SupporTicket, id=id)

    if request.method == "POST":
        form = SupporTicketForm(request.POST, instance=support_ticket)

        if form.is_valid():
            form.save()
            return redirect('support/ticket.html')
    else:
        form = SupporTicketForm(instance=support_ticket)

    context = {'form': form}
    return render(request, 'support/ticket.html', context)


def update_contract(request, id):  # обновляет  информацию о контаркте ссылку на компанию, назывние контракта и файл документа

    contracts = get_object_or_404(Contracts, id=id)

    if request.method == "POST":
        form = UpdateContractForm(request.POST, instance=contracts)

        if form.is_valid():
            form.save()
            return redirect('support/contracts.html')
    else:
        form = UpdateContractForm(instance=contracts)

    context = {'form': form}
    return render(request, 'support/contracts.html', context)


def primary_user_check(request, id):

        primary_user = get_object_or_404(User, id=id)

        if request.method == 'POST':
            form = PrimaryUserCheckForm(instance=primary_user)

            if form.is_valid():
                form.save()
                return redirect('support/users-list.html')

        else:
            form = PrimaryUserCheckForm(instance=primary_user)

        context = {'form': form}
        return render(request, 'support/users-list.html', context)


def company_check(request, id):

        company = get_object_or_404(Companies, id=id)

        if request.method == 'POST':

            form = CheckCompanyForm(request.POST, instance=company)
            if form.is_valid():
                form.save()
                return redirect('support/companies-list.html')

        else:
            form = CheckCompanyForm(instance=company)

        context = {'form': form}
        return render(request, 'support/companies-list.html', context)



def contract_check(request):

        contract = get_object_or_404(Contracts, id=request.POST.get('id'))

        if request.method == 'POST':

            form = CheckContractForm(request.POST, instance=contract)
            if form.is_valid():
                form.save()
                return redirect('support/contracts-list.html')

        else:
            form = CheckContractForm(instance=contract)

        context = {'form': form}
        return render(request, 'support/contracts-list.html', context)