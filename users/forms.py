from django.forms import ModelForm

from supports.models import SupporTicket, Contracts
from .models import User

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name','email', 'phone_number', 'message']

class TicketForm(ModelForm):
    class Meta:
        model = SupporTicket()
        fields = ['contract', 'description']

class ContractForm(ModelForm):
    class Meta:
        model = Contracts
        fields = ['']