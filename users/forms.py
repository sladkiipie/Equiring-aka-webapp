from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import SetPasswordForm

from supports.models import SupporTicket
from .models import User, Contracts, Companies


class PrimaryUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name','email', 'phone_number', 'message']

class CreateTicketForm(ModelForm):
    class Meta:
        model = SupporTicket
        fields = ['contract', 'description']
        widgets = {'contracts': forms.CheckboxSelectMultiple(),}

class CreateCompanyForm(ModelForm):
    class Meta:
        model = Companies
        fields = ['INN', 'OGRN', 'name_company']
        widgets = {'name_company': forms.CheckboxSelectMultiple(),}

class CreateContractForm(ModelForm):
    class Meta:
        model = Contracts
        fields = ['name_contract', 'company']
        widgets = {'company': forms.CheckboxSelectMultiple(),}