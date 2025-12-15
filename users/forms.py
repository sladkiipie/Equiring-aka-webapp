from django.forms import ModelForm
from django.contrib.auth.forms import SetPasswordForm

from supports.models import SupporTicket
from .models import User, Contracts, Companies


class PrimaryUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name','email', 'phone_number', 'message']

class TicketForm(ModelForm):
    class Meta:
        model = SupporTicket()
        fields = ['contract', 'description']

class CreateCompanyForm(ModelForm):
    class Meta:
        model = Companies
        fields = ['INN', 'OGRN', 'name_company']

class CreateContractForm(ModelForm):
    class Meta:
        model = Contracts
        fields = ['name_contract', 'company']
        
        
        