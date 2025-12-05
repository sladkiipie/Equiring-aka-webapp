from django.forms import ModelForm

from .models import SupporTicket
from users.models import Contracts, User


class SupporTicketForm(ModelForm):
    class Meta:
        model = SupporTicket
        fields = ['status']

class ContractForm(ModelForm):
    class Meta:
        model = Contracts
        fields = ['company', 'name', 'document']

class PrimaryUserCheckForm(ModelForm):
    class Meta:
        model = User
        fields = ['status']
