from django.forms import ModelForm

from .models import SupporTicket
from users.models import Contracts, User


class CheckTicketForm(ModelForm):
    class Meta:
        model = SupporTicket
        fields = ['status']

class CheckContractForm(ModelForm):
    class Meta:
        model = Contracts
        fields = ['status']


class CheckCompanyForm(ModelForm):
    class Meta:
        model = Contracts
        fields = []

class PrimaryUserCheckForm(ModelForm):
    class Meta:
        model = User
        fields = ['status']
