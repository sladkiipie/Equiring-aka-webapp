from django.shortcuts import redirect
from django.contrib import messages


from .forms import SupporTicketForm, ContractForm
from .models import SupporTicket

from users.models import Contracts




def update_support_ticket(request):
    try:
        support_ticket = SupporTicket.objects.get(id=id)
        form = SupporTicketForm(instance=support_ticket)
        if request.method == "POST":
            support_ticket.object.update(
                status=request.POST['status'],
            )
            return redirect(request, 'support/ticket.html')
        else:
            context = {'form': form}
            return redirect(request, 'support/ticket.html', context)
    except SupporTicket.DoesNotExist:
        messages.error(request, 'Support ticket not found.')

def updatet_contract(request):
    try:
        contracts = Contracts.object.get(id=id)
        form = ContractForm(instance=contracts)
        if request.method == "POST":
            Contracts.object.update(
                company=request.POST['company'],
                name=request.POST['name'],
                document=request.POST['document'],
            )
            return redirect(request, 'support/contracts.html')
        else:
            context = {'form': form}
            return redirect(request, 'support/contracts.html', context)
    except Contracts.DoesNotExist:
        messages.error(request, 'Contract not found.')