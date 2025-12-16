from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages


from .forms import CheckTicketForm, PrimaryUserCheckForm, CheckCompanyForm, CheckContractForm
from .models import SupporTicket

from users.models import Contracts, User, Companies


def support_page(request):
    return render(request, 'supports/supportpage.html')


def primary_user_check(request, id):

    primary_user = get_object_or_404(User, id=id)

    if request.method == 'POST':
        form = PrimaryUserCheckForm(instance=primary_user)

        if form.is_valid():
            form.save()
            return redirect('supports/users-list.html')

    else:
        form = PrimaryUserCheckForm(instance=primary_user)

    context = {'form': form}
    return render(request, 'supports/users-list.html', context)


def companies_page(request):
    return render(request, 'supports/company-list.html')

def company_check(request, id):

    company = get_object_or_404(Companies, id=id)

    if request.method == 'POST':

        form = CheckCompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect('supports/companies-list.html')

    else:
        form = CheckCompanyForm(instance=company)

    context = {'form': form}
    return render(request, 'supports/companies-list.html', context)


def tickets_page(request):
    return render(request, 'supports/ticket-list.html')

def ticket_check(request, id):  # изменяет статус тикета

    support_ticket = get_object_or_404(SupporTicket, id=id)

    if request.method == "POST":
        form = CheckTicketForm(request.POST, instance=support_ticket)

        if form.is_valid():
            form.save()
            return redirect('supports/ticket.html')
    else:
        form = CheckTicketForm(instance=support_ticket)

    context = {'form': form}
    return render(request, 'supports/ticket.html', context)


def contracts_page(request):
    return render(request, 'supports/contract-list.html')

def contract_check(request):

        contract = get_object_or_404(Contracts, id=request.POST.get('id'))

        if request.method == 'POST':

            form = CheckContractForm(request.POST, instance=contract)
            if form.is_valid():
                form.save()
                return redirect('supports/contracts-list.html')

        else:
            form = CheckContractForm(instance=contract)

        context = {'form': form}
        return render(request, 'supports/contracts-list.html', context)